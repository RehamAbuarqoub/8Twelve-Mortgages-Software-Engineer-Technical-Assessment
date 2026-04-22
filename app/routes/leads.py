from flask import Blueprint, jsonify, request
from uuid import uuid4
from app.store import leads_db

leads_bp = Blueprint("leads", __name__)


def is_valid_email(email):
    return isinstance(email, str) and "@" in email and "." in email


def is_valid_phone(phone):
    return isinstance(phone, str) and len(phone.strip()) >= 7


@leads_bp.route("/leads", methods=["POST"])
def create_lead():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    source = data.get("source")
    status = data.get("status", "new")

    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    if not source or not isinstance(source, str) or not source.strip():
        return jsonify({"error": "Source is required"}), 400

    if not email and not phone:
        return jsonify({"error": "At least one contact field is required: email or phone"}), 400

    if email and not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    if phone and not is_valid_phone(phone):
        return jsonify({"error": "Invalid phone format"}), 400

    lead_id = str(uuid4())

    new_lead = {
        "id": lead_id,
        "name": name.strip(),
        "email": email,
        "phone": phone,
        "source": source.strip(),
        "status": status,
        "summary": None
    }

    leads_db[lead_id] = new_lead

    return jsonify(new_lead), 201


@leads_bp.route("/leads", methods=["GET"])
def get_leads():
    source = request.args.get("source")
    status = request.args.get("status")

    leads = list(leads_db.values())

    if source:
        leads = [lead for lead in leads if lead["source"].lower() == source.lower()]

    if status:
        leads = [lead for lead in leads if lead["status"].lower() == status.lower()]

    return jsonify(leads), 200


@leads_bp.route("/leads/<lead_id>", methods=["GET"])
def get_lead_by_id(lead_id):
    lead = leads_db.get(lead_id)

    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    return jsonify(lead), 200