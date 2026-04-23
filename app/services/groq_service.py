from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL


# AI Option A:
# This function creates a short summary for a new lead using Groq.
def generate_lead_summary(lead_data):
    # Stop if the Groq API key is missing
    if not GROQ_API_KEY:
        return "AI summary unavailable: missing Groq API key."

    try:
        # Create the Groq client
        client = Groq(api_key=GROQ_API_KEY)

        # AI Option A:
        # Build the prompt that asks Groq to write a short lead summary
        prompt = f"""
You are helping assess a mortgage lead.

Based on the following lead information, write a short 2-3 sentence lead assessment summary.

Lead details:
- Name: {lead_data.get("name")}
- Email: {lead_data.get("email")}
- Phone: {lead_data.get("phone")}
- Source: {lead_data.get("source")}
- Status: {lead_data.get("status")}

Keep the summary concise, professional, and useful for a sales or intake team.
"""

        # AI Option A:
        # Send the lead data to Groq and get the summary back
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You write short lead assessment summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=120
        )

        # Return the AI summary text
        return response.choices[0].message.content.strip()

    except Exception:
        # Return a fallback message if the AI request fails
        return "AI summary unavailable due to Groq API failure."