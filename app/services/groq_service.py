from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL


def generate_lead_summary(lead_data):
    if not GROQ_API_KEY:
        return "AI summary unavailable: missing Groq API key."

    try:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are helping assess a mortgage lead.

Based on the following lead information, write a short 2-3 sentence lead assessment summary.

Lead details:
- Name: {lead_data.get("name")}
- Email: {lead_data.get("email")}
- Phone: {lead_data.get("phone")}
- Source: {lead_data.get("source")}
- Status: {lead_data.get("status")}

Rules:
1. Return only the summary text.
2. Do not add titles, headings, labels, quotation marks, or introductions.
3. Do not say phrases like "Here’s a summary" or "Lead Assessment Summary".
4. Use only the provided details.
5. Do not assume intent, interest level, or any missing information.
6. If contact details appear unusual or unclear, mention that they may need verification.
7. Keep it concise, clear, and professional.
"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You write short lead assessment summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=120
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "AI summary unavailable due to Groq API failure."


def generate_next_step_suggestion(lead_data):
    if not GROQ_API_KEY:
        return "AI next step suggestion unavailable: missing Groq API key."

    try:
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""
You are helping assess a mortgage lead.

Based on the following lead information, suggest one short and practical next step for the sales or intake team.

Lead details:
- Name: {lead_data.get("name")}
- Email: {lead_data.get("email")}
- Phone: {lead_data.get("phone")}
- Source: {lead_data.get("source")}
- Status: {lead_data.get("status")}

Rules:
1. Return only the suggestion text.
2. Do not add titles, headings, labels, quotation marks, or introductions.
3. Use only the provided details.
4. Do not assume intent, urgency, budget, or any missing information.
5. Keep it short, clear, practical, and professional.
6. If the information is limited or unclear, suggest a simple follow-up or verification step.
"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You write short and practical next-step suggestions for new leads."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=60
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "AI next step suggestion unavailable due to Groq API failure."