# fetch_bills.py
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CONGRESS_API_KEY = os.getenv("CONGRESS_API_KEY")

# Base URL for Congress API
BASE_URL = "https://api.congress.gov/v3/bill"

def fetch_recent_bills(limit=5):
    """Fetch recent federal bills from Congress.gov API."""
    params = {
        "api_key": CONGRESS_API_KEY,
        "limit": limit,
        "format": "json"  # Ensure JSON response
    }
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
            data = response.json()
            print("🔹 API Response:\n", data)  # Print full response for debugging
            return data
    else:
        print(f"❌ Error fetching data: {response.status_code}")
        return None

if __name__ == "__main__":
    bills = fetch_recent_bills()
    print(bills)  # Test API output
