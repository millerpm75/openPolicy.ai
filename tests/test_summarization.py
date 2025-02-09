import openai
import os

# Load API key from environment variable (recommended for security)
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    """Use OpenAI to generate a concise summary of legislative text."""
    prompt = f"Summarize this legislation in 2-3 sentences:\n\n{text}"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
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

# Test Bill Text
bill_text = """The HALT Fentanyl Act aims to permanently classify fentanyl-related substances as Schedule I drugs 
under the Controlled Substances Act. This legislation seeks to strengthen law enforcement's ability to combat 
fentanyl trafficking while ensuring medical research can continue under regulated guidelines."""

# Test Executive Order Text
eo_text = """The Executive Order on Unleashing Prosperity Through Deregulation directs federal agencies 
to reduce regulatory burdens on businesses by eliminating outdated and unnecessary rules. The order 
emphasizes economic growth, job creation, and innovation while maintaining essential protections."""

# Generate summaries
bill_summary = summarize_text(bill_text)
eo_summary = summarize_text(eo_text)

# Print results
print(f"📜 **Bill Summary (HALT Fentanyl Act):** {bill_summary}\n")
print(f"📜 **EO Summary (Unleashing Prosperity Through Deregulation):** {eo_summary}\n")
