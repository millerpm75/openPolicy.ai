import requests

# Updated Federal Register API endpoint for Executive Orders
API_URL = "https://www.federalregister.gov/api/v1/documents"

def fetch_executive_orders():
    """Fetch recent executive orders from the Federal Register API."""
    params = {
        "per_page": 5,         # Limit to 5 results for testing
        "order": "newest",     # Get the most recent EOs
        "type[]": "Executive Order",  # Filter for Executive Orders
        "fields[]": ["title", "document_number", "publication_date", "full_text_xml_url"]
    }

    response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        print("✅ API Response:")
        for eo in data.get("results", []):
            print(f"\n📜 Executive Order: {eo.get('title')}")
            print(f"🔹 Document Number: {eo.get('document_number')}")
            print(f"📅 Published On: {eo.get('publication_date')}")
            print(f"🔗 Full Text: {eo.get('full_text_xml_url', 'No URL available')}")
    else:
        print(f"❌ API Request Failed. Status Code: {response.status_code}")
        print(response.text)

# Run the test
fetch_executive_orders()
