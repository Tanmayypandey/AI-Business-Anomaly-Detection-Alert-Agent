import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env file")
    exit()

print("🔑 API key loaded successfully!")

# Create OpenAI client
client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-5-mini",
        input="Reply with exactly: AI connection successful!"
    )

    print("\n🤖 AI Response:")
    print(response.output_text)

    print("\n✅ OpenAI API connection successful!")

except Exception as e:
    print("\n❌ API connection failed!")
    print("Error:", e)