import openai
import os

# Ensure API key is set correctly
openai.api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")

def summarize_text(text):
    """Use OpenAI to generate a concise summary of legislative text."""
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

# Test EO
eo_text = "Continuation of the National Emergency With Respect to the Situation in and in Relation to Burma"
eo_summary = summarize_text(eo_text)

print(f"📜 **EO Summary:** {eo_summary}")
