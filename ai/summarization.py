# summarization.py
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def summarize_bill(text):
    """Use OpenAI GPT to summarize a bill."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Summarize this legal bill in plain English."},
                  {"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    test_text = "This bill aims to reduce corporate tax rates for small businesses..."
    print(summarize_bill(test_text))  # Test summarization
