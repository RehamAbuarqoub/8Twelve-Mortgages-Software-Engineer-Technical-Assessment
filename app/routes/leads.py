from flask import Blueprint, jsonify, request
from uuid import uuid4

from app.store import leads_db
from app.services.groq_service import generate_lead_summary

# This blueprint holds all lead routes
leads_bp = Blueprint("leads", __name__)


def is_valid_email(email):
    # Check if the email looks valid
    return isinstance(email, str) and "@" in email and "." in email


def is_valid_phone(phone):
    # Check if the phone number is long enough
    return isinstance(phone, str) and len(phone.strip()) >= 7


@leads_bp.route("/leads", methods=["POST"])
def create_lead():
    # Get JSON data from the request
    data = request.get_json()

    # Stop if the request body is not valid JSON
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Get lead details from the request
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    source = data.get("source")
    status = data.get("status", "new")

    # Make sure name is given
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Name is required"}), 400

    # Make sure source is given
    if not source or not isinstance(source, str) or not source.strip():
        return jsonify({"error": "Source is required"}), 400

    # Make sure there is at least one way to contact the lead
    if not email and not phone:
        return jsonify({"error": "At least one contact field is required: email or phone"}), 400

    # Check email if it is included
    if email and not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Check phone if it is included
    if phone and not is_valid_phone(phone):
        return jsonify({"error": "Invalid phone format"}), 400

    # Create a unique ID for this lead
    lead_id = str(uuid4())

    # Create the lead record
    new_lead = {
        "id": lead_id,
        "name": name.strip(),
        "email": email,
        "phone": phone,
        "source": source.strip(),
        "status": status,
        "summary": None
    }

    # AI section (Option A):
    # Create a short lead summary using Groq and save it with the lead
    new_lead["summary"] = generate_lead_summary(new_lead)

    # Save the lead in memory
    leads_db[lead_id] = new_lead

    # Send back the saved lead
    return jsonify(new_lead), 201


@leads_bp.route("/leads", methods=["GET"])
def get_leads():
    # Get filter values from the URL
    source = request.args.get("source")
    status = request.args.get("status")

    # Start with all saved leads
    leads = list(leads_db.values())

    # Filter by source if needed
    if source:
        leads = [lead for lead in leads if lead["source"].lower() == source.lower()]

    # Filter by status if needed
    if status:
        leads = [lead for lead in leads if lead["status"].lower() == status.lower()]

    # Send back the final list
    return jsonify(leads), 200


@leads_bp.route("/leads/<lead_id>", methods=["GET"])
def get_lead_by_id(lead_id):
    # Find the lead using its ID
    lead = leads_db.get(lead_id)

    # Show an error if the lead is not found
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    # Send back the lead
    return jsonify(lead), 200