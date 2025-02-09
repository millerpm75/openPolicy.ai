# store_executive_orders.py
# import requests
# from database.db_connection import SessionLocal
# from database.models import ExecutiveOrder
# from sqlalchemy import func

# # API endpoint
# API_URL = "https://www.federalregister.gov/api/v1/documents"

# def fetch_and_store_executive_orders():
#     """Fetch recent Executive Orders and store them in the database."""
#     session = SessionLocal()

#     try:
#         params = {
#             "per_page": 10,  # Fetch 10 results
#             "order": "newest",
#             "type[]": "Executive Order",
#             "fields[]": ["title", "document_number", "publication_date", "full_text_xml_url"]
#         }

#         response = requests.get(API_URL, params=params)
        
#         if response.status_code != 200:
#             print(f"❌ API Request Failed. Status Code: {response.status_code}")
#             return

#         data = response.json()
#         new_count = 0  # Track new insertions

#         for eo in data.get("results", []):
#             eo_number = eo.get("document_number")
#             title = eo.get("title")
#             issued_date = eo.get("publication_date")
#             full_text_url = eo.get("full_text_xml_url", "")

#             # Check for duplicate entry
#             existing_eo = session.query(ExecutiveOrder).filter(
#                 func.lower(ExecutiveOrder.eo_number) == eo_number.lower()
#             ).first()

#             if existing_eo:
#                 print(f"⚠️ Skipping duplicate: {eo_number} - {title}")
#                 continue  # Skip duplicate

#             # Insert new EO into the database
#             new_eo = ExecutiveOrder(
#                 eo_number=eo_number,
#                 title=title,
#                 issued_date=issued_date,
#                 full_text_url=full_text_url
#             )
#             session.add(new_eo)
#             new_count += 1

#             print(f"✅ Added EO: {eo_number} - {title}")

#         # Commit only if new orders were added
#         if new_count > 0:
#             session.commit()
#             print(f"📌 {new_count} new Executive Orders stored in the database.")
#         else:
#             print("⚠️ No new Executive Orders added.")

#     except Exception as e:
#         print(f"❌ Error processing EOs: {e}")

#     finally:
#         session.close()

# # Run the function
# if __name__ == "__main__":
#     fetch_and_store_executive_orders()

import openai
import os
from database.session import SessionLocal
from database.models import ExecutiveOrder
from api.services.fetch_executive_orders import fetch_executive_orders

# Ensure API key is set correctly
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    """Use OpenAI to generate a concise summary of an Executive Order."""
    prompt = f"Summarize this executive order in 2-3 sentences:\n\n{text}"

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

def store_executive_orders():
    """Fetch and store recent executive orders with AI-generated summaries."""
    session = SessionLocal()
    eos_data = fetch_executive_orders()
    
    if not eos_data:
        print("🚨 ERROR: API response is None!")
        return

    if not isinstance(eos_data, dict):
        print("🚨 ERROR: Unexpected response format:", type(eos_data))
        return

    if "results" not in eos_data:
        print("🚨 ERROR: 'results' key missing from response. Full response:", eos_data)
        return

    print("Raw API Response:", eos_data)

    for eo in eos_data["results"]:
        eo_number = eo["document_number"]
        existing_eo = session.query(ExecutiveOrder).filter(ExecutiveOrder.eo_number == eo_number).first()

        if existing_eo:
            print(f"⚠️ Skipping duplicate (found in DB): {eo_number}")
            continue

        print(f"✅ Adding new Executive Order: {eo_number} - {eo['title']}")

        ai_summary = summarize_text(eo["title"])

        new_eo = ExecutiveOrder(
            eo_number=eo_number,
            title=eo["title"],
            summary=ai_summary,  # 🔹 AI-generated summary
            issued_date=eo["publication_date"],
            full_text_url=eo["full_text_xml_url"]
        )

        session.add(new_eo)

    session.commit()
    print(f"✅ Successfully stored {len(eos_data['results'])} executive orders with AI summaries.")
    session.close()

if __name__ == "__main__":
    store_executive_orders()