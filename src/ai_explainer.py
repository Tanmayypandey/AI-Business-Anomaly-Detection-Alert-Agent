import requests
import pandas as pd


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


# ==================================================
# ASK LOCAL AI
# ==================================================

def ask_ai(prompt):
    """
    Send a prompt to the local Ollama model
    and return the AI-generated response.
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "").strip()

    except requests.exceptions.ConnectionError:

        return "❌ Ollama is not running. Please start Ollama first."

    except requests.exceptions.Timeout:

        return "❌ AI request timed out."

    except Exception as e:

        return f"❌ AI request failed: {e}"


# ==================================================
# BUILD INCIDENT PROMPT
# ==================================================

def build_incident_prompt(incident_df):
    """
    Convert an incident dataframe into a structured
    prompt for the local AI model.
    """

    incident_text = ""

    for _, row in incident_df.iterrows():

        incident_text += f"""
Metric: {row['Metric']}
Date: {row['Date']}
Value: {row['Value']}
Baseline: {row['Baseline']}
Change: {row['Change_%']:.2f}%
Direction: {row['Direction']}
Severity: {row['Severity']}
"""


    prompt = f"""
You are an experienced business data analyst.

Analyze the following business anomaly incident.

INCIDENT DATA:
{incident_text}

Your task is to provide a concise business analysis.

IMPORTANT RULES:

- Use ONLY the facts, dates, metrics, and numbers provided in INCIDENT DATA.
- Never invent dates, months, baseline periods, customers, products, campaigns, or business events.
- Do not say that the baseline belongs to a specific month unless that information is explicitly provided.
- Do not invent a specific cause.
- If the actual cause is unknown, clearly say that it is unknown and provide only possible causes.
- Keep all numerical values exactly consistent with the provided data.
- Do not change or reinterpret the supplied dates or values.
- Do not assume information that is not present in INCIDENT DATA.

Return exactly these four sections:

BUSINESS INSIGHT:
Explain what happened using the provided metrics.

POSSIBLE CAUSE:
Give realistic possible reasons for the observed movement.
Do not present possible causes as confirmed facts.

BUSINESS IMPACT:
Explain why this anomaly may matter to the business.

RECOMMENDED ACTION:
Give practical actions a business analyst or manager should take.

Keep the response concise, professional, and easy for a non-technical
business manager to understand.
"""

    return prompt


# ==================================================
# ANALYZE INCIDENT WITH AI
# ==================================================

def analyze_incident_with_ai(incident_df):
    """
    Analyze a real incident using the local Llama 3.2 model.
    """

    prompt = build_incident_prompt(incident_df)

    ai_response = ask_ai(prompt)

    return ai_response


# ==================================================
# TEST LOCAL AI
# ==================================================

if __name__ == "__main__":

    print("\n🤖 Testing AI with incident data...\n")

    # Example incident data
    test_incident = pd.DataFrame([
        {
            "Metric": "Revenue",
            "Date": "2026-03-31",
            "Value": 2117442.64,
            "Baseline": 1458246.41,
            "Change_%": 45.20,
            "Direction": "Increase",
            "Severity": "HIGH"
        },
        {
            "Metric": "Orders",
            "Date": "2026-03-31",
            "Value": 1867,
            "Baseline": 1280.86,
            "Change_%": 45.76,
            "Direction": "Increase",
            "Severity": "HIGH"
        }
    ])

    # Send incident to AI
    result = analyze_incident_with_ai(test_incident)

    print("=" * 70)
    print("🤖 AI BUSINESS ANALYSIS")
    print("=" * 70)

    print(result)

    print("=" * 70)

    print("\n✅ AI incident test completed!")