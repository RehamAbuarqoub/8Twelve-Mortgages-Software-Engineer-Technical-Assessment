import pytest
from app.app import app
from app.store import leads_db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        leads_db.clear()
        yield client
        leads_db.clear()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_lead_success(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    payload = {
        "name": "John Smith",
        "email": "john@example.com",
        "source": "website"
    }

    response = client.post("/leads", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["name"] == "John Smith"
    assert data["email"] == "john@example.com"
    assert data["source"] == "website"
    assert data["status"] == "new"
    assert data["summary"] == "Test AI summary"
    assert "id" in data


def test_create_lead_missing_name(client):
    payload = {
        "email": "john@example.com",
        "source": "website"
    }

    response = client.post("/leads", json=payload)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Name is required"


def test_create_lead_missing_source(client):
    payload = {
        "name": "John Smith",
        "email": "john@example.com"
    }

    response = client.post("/leads", json=payload)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Source is required"


def test_create_lead_missing_contact(client):
    payload = {
        "name": "John Smith",
        "source": "website"
    }

    response = client.post("/leads", json=payload)
    assert response.status_code == 400
    assert response.get_json()["error"] == "At least one contact field is required: email or phone"


def test_get_all_leads(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    client.post("/leads", json={
        "name": "John Smith",
        "email": "john@example.com",
        "source": "website"
    })

    client.post("/leads", json={
        "name": "Sarah Ali",
        "phone": "1234567890",
        "source": "facebook",
        "status": "contacted"
    })

    response = client.get("/leads")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


def test_filter_leads_by_source(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    client.post("/leads", json={
        "name": "John Smith",
        "email": "john@example.com",
        "source": "website"
    })

    client.post("/leads", json={
        "name": "Sarah Ali",
        "phone": "1234567890",
        "source": "facebook"
    })

    response = client.get("/leads?source=website")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["source"] == "website"


def test_filter_leads_by_status(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    client.post("/leads", json={
        "name": "John Smith",
        "email": "john@example.com",
        "source": "website",
        "status": "new"
    })

    client.post("/leads", json={
        "name": "Sarah Ali",
        "phone": "1234567890",
        "source": "facebook",
        "status": "contacted"
    })

    response = client.get("/leads?status=contacted")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["status"] == "contacted"


def test_get_single_lead_by_id(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    create_response = client.post("/leads", json={
        "name": "John Smith",
        "email": "john@example.com",
        "source": "website"
    })

    lead_id = create_response.get_json()["id"]

    response = client.get(f"/leads/{lead_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == lead_id
    assert data["name"] == "John Smith"


def test_get_single_lead_not_found(client):
    response = client.get("/leads/non-existent-id")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Lead not found"