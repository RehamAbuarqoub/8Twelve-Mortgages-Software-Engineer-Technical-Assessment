import pytest
from app.app import app
from app.store import leads_db


# -------------------------
# Test setup
# -------------------------

@pytest.fixture
def client():
    # Turn on testing mode
    app.config["TESTING"] = True

    # Create a test client
    with app.test_client() as client:
        # Clear saved leads before each test
        leads_db.clear()
        yield client
        # Clear saved leads after each test
        leads_db.clear()


def sample_lead(**changes):
    # Default valid lead data
    lead = {
        "name": "John Smith",
        "email": "john@example.com",
        "source": "website"
    }

    # Update any field if needed
    lead.update(changes)
    return lead


# -------------------------
# Health route tests
# -------------------------

def test_health(client):
    # Check that /health works
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


# -------------------------
# POST /leads tests
# -------------------------

def test_create_lead_success(client, monkeypatch):
    # Use a fake AI summary instead of calling the real API
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    response = client.post("/leads", json=sample_lead())
    data = response.get_json()

    # Check that the lead was created
    assert response.status_code == 201
    assert data["name"] == "John Smith"
    assert data["email"] == "john@example.com"
    assert data["source"] == "website"
    assert data["status"] == "new"
    assert data["summary"] == "Test AI summary"
    assert "id" in data


def test_create_lead_missing_name(client):
    # Send lead data without a name
    payload = sample_lead()
    payload.pop("name")

    response = client.post("/leads", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Name is required"


def test_create_lead_missing_source(client):
    # Send lead data without a source
    payload = sample_lead()
    payload.pop("source")

    response = client.post("/leads", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "Source is required"


def test_create_lead_missing_contact(client):
    # Send lead data without email and phone
    payload = {
        "name": "John Smith",
        "source": "website"
    }

    response = client.post("/leads", json=payload)

    assert response.status_code == 400
    assert response.get_json()["error"] == "At least one contact field is required: email or phone"


def test_create_lead_with_groq_failure_fallback(client, monkeypatch):
    # Fake a Groq failure message
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "AI summary unavailable due to Groq API failure."
    )

    response = client.post("/leads", json=sample_lead())
    data = response.get_json()

    # Check that the lead is still created
    assert response.status_code == 201
    assert data["summary"] == "AI summary unavailable due to Groq API failure."


# -------------------------
# GET /leads tests
# -------------------------

def test_get_all_leads(client, monkeypatch):
    # Use a fake AI summary
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    # Create two leads
    client.post("/leads", json=sample_lead())
    client.post("/leads", json=sample_lead(
        name="Sarah Ali",
        email=None,
        phone="1234567890",
        source="facebook",
        status="contacted"
    ))

    response = client.get("/leads")
    data = response.get_json()

    # Check that both leads are returned
    assert response.status_code == 200
    assert len(data) == 2


def test_filter_leads_by_source(client, monkeypatch):
    # Use a fake AI summary
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    # Create two leads with different sources
    client.post("/leads", json=sample_lead(source="website"))
    client.post("/leads", json=sample_lead(
        name="Reham Omar",
        email=None,
        phone="1234567890",
        source="facebook"
    ))

    response = client.get("/leads?source=website")
    data = response.get_json()

    # Check that only website leads are returned
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["source"] == "website"


def test_filter_leads_by_status(client, monkeypatch):
    # Use a fake AI summary
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    # Create two leads with different status values
    client.post("/leads", json=sample_lead(status="new"))
    client.post("/leads", json=sample_lead(
        name="Reham Omar",
        email=None,
        phone="1234567890",
        source="facebook",
        status="contacted"
    ))

    response = client.get("/leads?status=contacted")
    data = response.get_json()

    # Check that only contacted leads are returned
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["status"] == "contacted"


# -------------------------
# GET /leads/<id> tests
# -------------------------

def test_get_single_lead_by_id(client, monkeypatch):
    # Use a fake AI summary
    monkeypatch.setattr(
        "app.routes.leads.generate_lead_summary",
        lambda lead: "Test AI summary"
    )

    # Create one lead
    create_response = client.post("/leads", json=sample_lead())
    lead_id = create_response.get_json()["id"]

    response = client.get(f"/leads/{lead_id}")
    data = response.get_json()

    # Check that the correct lead is returned
    assert response.status_code == 200
    assert data["id"] == lead_id
    assert data["name"] == "John Smith"


def test_get_single_lead_not_found(client):
    # Ask for a lead that does not exist
    response = client.get("/leads/non-existent-id")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Lead not found"