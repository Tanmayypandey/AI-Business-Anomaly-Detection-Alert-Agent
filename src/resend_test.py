import os
from dotenv import load_dotenv
import resend

# Load .env file
load_dotenv()

# Get API key
resend.api_key = os.getenv("RESEND_API_KEY")

receiver_email = os.getenv("ALERT_RECEIVER_EMAIL")

print("\n📧 Testing Resend email connection...\n")

if not resend.api_key:
    print("❌ RESEND_API_KEY not found in .env")
    exit()

if not receiver_email:
    print("❌ ALERT_RECEIVER_EMAIL not found in .env")
    exit()

try:
    params = {
        "from": "AI Business Anomaly Agent <onboarding@resend.dev>",
        "to": [receiver_email],
        "subject": "🚨 AI Business Anomaly Agent - Test Email",
        "html": """
        <h2>🤖 AI Business Anomaly Agent</h2>

        <p>This is a test email from your AI Business Anomaly Detection project.</p>

        <p>✅ Resend API connection is working successfully.</p>

        <p><b>Email Alert System:</b> READY</p>
        """
    }

    response = resend.Emails.send(params)

    print("✅ Email sent successfully!")
    print("Response:", response)

except Exception as e:
    print("❌ Email sending failed!")
    print("Error:", e)