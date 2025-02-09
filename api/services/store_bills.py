# store_bills.py
from api.services.fetch_bills import fetch_recent_bills
from database.session import SessionLocal
from database.models import Bill
from sqlalchemy import func
import openai
import os

# Ensure API key is set correctly
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    """Use OpenAI to generate a concise summary of legislative text."""
    prompt = f"Summarize this bill in 2-3 sentences:\n\n{text}"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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


# def store_bills():

#     """Fetch and store bills in the PostgreSQL database."""
#     session = SessionLocal()
#     bills_data = fetch_recent_bills()

#     if not bills_data or "bills" not in bills_data:
#         print("❌ No valid bill data retrieved.")
#         return

#     added_count = 0

#     for bill in bills_data["bills"]:
#         try:
#             bill_id = (bill.get("type", "Unknown") + str(bill.get("number", "Unknown"))).upper().strip()
#             # Print to debug duplicate check
#             print(f"🔍 Checking for existing bill_id: {bill_id}")

#             title = bill.get("title", "No title available")

#             # Check if the bill already exists
#             existing_bill = session.query(Bill).filter(func.lower(Bill.bill_id) == bill_id.lower()).first()

#             if existing_bill:
#                 print(f"⚠️ Skipping duplicate (found in DB): {existing_bill.bill_id}")
#                 continue  # This should prevent duplicate inserts

#             print(f"✅ Inserting new bill: {bill_id}")  # Log when an insert is happening

#             bill_entry = Bill(
#                 bill_id=bill_id,
#                 title=title,
#                 summary="No summary available",  # Congress API doesn’t provide summaries in this call
#                 status=bill.get("latestAction", {}).get("text", "No status available"),
#                 sponsor="Unknown",  # No sponsor data in this API call
#                 introduced_date=bill.get("latestAction", {}).get("actionDate", None),
#                 last_action=bill.get("latestAction", {}).get("text", "No last action available"),
#                 full_text_url=bill.get("url", "No link available")
#             )

#             session.add(bill_entry)
#             added_count += 1
#             print(f"✅ Added bill: {bill_id} - {title}")

#         except Exception as e:
#             print(f"❌ Error processing bill: {bill} - {e}")

#     print(f"📊 Session new objects before commit: {session.new}")  # Check what's staged for commit

#     if added_count > 0:
#         session.commit()  # Ensure data is actually saved
#         print(f"✅ {added_count} new bills successfully stored in the database.")
    
#        # Check database immediately after commit
#         check_bills = session.query(Bill).all()
#         print(f"📌 Database check: {len(check_bills)} bills found.")
#     else:
#         print("⚠️ No new bills were added (all duplicates).") 

#     session.close()

def store_bills():
    """Fetch and store recent bills with AI-generated summaries."""
    session = SessionLocal()
    bills_data = fetch_recent_bills()

    for bill in bills_data["bills"]:
        bill_id = f"{bill['type']}{bill['number']}"
        existing_bill = session.query(Bill).filter(Bill.bill_id == bill_id).first()

        if existing_bill:
            print(f"⚠️ Skipping duplicate (found in DB): {bill_id}")
            continue

        print(f"✅ Adding new bill: {bill_id} - {bill['title']}")

        ai_summary = summarize_text(bill["title"])

        new_bill = Bill(
            bill_id=bill_id,
            title=bill["title"],
            summary=ai_summary,  # 🔹 AI-generated summary
            status=bill["latestAction"]["text"],
            sponsor="Unknown",
            introduced_date=bill["latestAction"]["actionDate"],
            last_action=bill["latestAction"]["text"],
            full_text_url=bill["url"],
            legislation_level="federal",
            jurisdiction="N/A"
        )

        session.add(new_bill)

    session.commit()
    print(f"✅ Successfully stored {len(bills_data['bills'])} bills with AI summaries.")
    session.close()


if __name__ == "__main__":
    store_bills()  # Run the function to store bills
