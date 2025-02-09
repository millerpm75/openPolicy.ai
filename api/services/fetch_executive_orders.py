# fetch_executive_orders.py
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

    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    if response.status_code != 200:
        print(f"🚨 Error: API request failed with status code {response.status_code}")
        return None

    if response.status_code == 200:
        try:
            data = response.json()
            print("🚀 DEBUG: Raw Parsed JSON Response:", data)  # 🔹 Check if "results" exists
            return data
        
            print("✅ API Response:")
            for eo in data.get("results", []):
                print(f"\n📜 Executive Order: {eo.get('title')}")
                print(f"🔹 Document Number: {eo.get('document_number')}")
                print(f"📅 Published On: {eo.get('publication_date')}")
                print(f"🔗 Full Text: {eo.get('full_text_xml_url', 'No URL available')}")
        except ValueError:
            print("🚨 Error: Failed to parse JSON response")
            return None
    else:
        print(f"❌ API Request Failed. Status Code: {response.status_code}")
        print(response.text)
        print("Parsed API Response:", data)

# Run the test
if __name__ == "__main__":
    print(fetch_executive_orders())
