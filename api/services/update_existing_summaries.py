import openai
import os
from database.session import SessionLocal
from database.models import Bill, ExecutiveOrder
from sqlalchemy import func

# Ensure API key is set correctly
openai.api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")

def summarize_text(text):
    """Use OpenAI to generate a concise summary of legislative text."""
    prompt = f"Summarize this legislation in 2-3 sentences:\n\n{text}"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Change to gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a legal analyst summarizing government policies."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return "Summary unavailable."

def update_bill_summaries():
    """Find all bills with 'No summary available' and update them with AI-generated summaries."""
    session = SessionLocal()
    bills = session.query(Bill).filter(func.lower(Bill.summary) == "no summary available").all()

    for bill in bills:
        print(f"🔍 Generating summary for: {bill.bill_id} - {bill.title}")
        bill.summary = summarize_text(bill.title)  # Using title as input for AI
        session.add(bill)

    if bills:
        session.commit()
        print(f"✅ Updated {len(bills)} bills with AI-generated summaries.")
    else:
        print("⚠️ No bills needed updating.")

    session.close()

def update_eo_summaries():
    """Find all Executive Orders with 'No summary available' and update them with AI-generated summaries."""
    session = SessionLocal()
    eos = session.query(ExecutiveOrder).filter(func.coalesce(ExecutiveOrder.summary, '') == '').all()

    for eo in eos:
        print(f"🔍 Generating summary for EO: {eo.eo_number} - {eo.title}")
        generated_summary = summarize_text(eo.title)  # Generate AI summary

        # DEBUG PRINT TO CONFIRM
        print(f"✅ Summary Generated: {generated_summary}")

        eo.summary = generated_summary
        session.add(eo)

    if eos:
        session.commit()
        print(f"✅ Updated {len(eos)} Executive Orders with AI-generated summaries.")
    else:
        print("⚠️ No Executive Orders needed updating.")

    session.close()


if __name__ == "__main__":
    update_bill_summaries()
    update_eo_summaries()
