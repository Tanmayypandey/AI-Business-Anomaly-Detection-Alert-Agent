import pandas as pd


# ==================================================
# ALERT ENGINE
# ==================================================

def get_alert_level(severity):

    severity = str(severity).upper()

    if severity == "HIGH":
        return "🔴 HIGH"

    elif severity == "MEDIUM":
        return "🟠 MEDIUM"

    elif severity == "LOW":
        return "🟢 LOW"

    else:
        return "⚪ UNKNOWN"


def generate_alert(incident_id, incident_df, ai_response):

    if incident_df.empty:
        return "No anomaly detected."

    # ----------------------------------------------
    # Basic incident information
    # ----------------------------------------------

    date = incident_df["Date"].iloc[0]

    if hasattr(date, "strftime"):
        date = date.strftime("%Y-%m-%d")

    metrics = ", ".join(
        incident_df["Metric"].astype(str).tolist()
    )

    # Highest severity in the incident
    severity_order = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3
    }

    highest_severity = max(
        incident_df["Severity"],
        key=lambda x: severity_order.get(
            str(x).upper(),
            0
        )
    )

    alert_level = get_alert_level(
        highest_severity
    )

    # ----------------------------------------------
    # Build alert
    # ----------------------------------------------

    alert = f"""
============================================================
🚨 BUSINESS ANOMALY ALERT
============================================================

Incident ID : {incident_id}
Date        : {date}
Metrics     : {metrics}
Severity    : {alert_level}

------------------------------------------------------------
📊 ANOMALY DETAILS
------------------------------------------------------------
"""

    for _, row in incident_df.iterrows():

        change = row["Change_%"]

        direction = row["Direction"]

        alert += f"""
Metric      : {row["Metric"]}
Value       : {row["Value"]:.2f}
Baseline    : {row["Baseline"]:.2f}
Change      : {change:.2f}%
Direction   : {direction}
Severity    : {row["Severity"]}
------------------------------------------------------------
"""

    # ----------------------------------------------
    # Add AI analysis
    # ----------------------------------------------

    alert += f"""
🤖 AI BUSINESS ANALYSIS
============================================================

{ai_response}

============================================================
⚠️ ALERT STATUS: {alert_level}
============================================================
"""

    return alert


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    print("\n🚨 Alert Engine Test")

    test_data = pd.DataFrame([
        {
            "Metric": "Revenue",
            "Date": "2025-08-11",
            "Value": 2173512.59,
            "Baseline": 1461626.51,
            "Change_%": 48.71,
            "Direction": "Increase",
            "Severity": "HIGH"
        }
    ])

    test_ai_response = """
BUSINESS INSIGHT:
Revenue increased significantly compared
to the baseline.

POSSIBLE CAUSE:
Possible increase in demand or successful
marketing activity.

BUSINESS IMPACT:
The increase may indicate a positive
business opportunity.

RECOMMENDED ACTION:
Investigate the reason for the increase
and monitor future revenue.
"""

    alert = generate_alert(
        "INC-001",
        test_data,
        test_ai_response
    )

    print(alert)