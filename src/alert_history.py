import os
import pandas as pd
from datetime import datetime


# ============================================================
# ALERT HISTORY CONFIGURATION
# ============================================================

HISTORY_FOLDER = "reports"
HISTORY_FILE = os.path.join(
    HISTORY_FOLDER,
    "alert_history.csv"
)


# ============================================================
# INITIALIZE ALERT HISTORY FILE
# ============================================================

def initialize_alert_history():
    """
    Create alert history CSV if it does not exist.
    """

    os.makedirs(
        HISTORY_FOLDER,
        exist_ok=True
    )

    if not os.path.exists(HISTORY_FILE):

        columns = [
            "Incident_ID",
            "Date",
            "Severity",
            "Metrics",
            "Email_Status",
            "Email_ID",
            "Sent_At"
        ]

        df = pd.DataFrame(
            columns=columns
        )

        df.to_csv(
            HISTORY_FILE,
            index=False
        )


# ============================================================
# CHECK WHETHER ALERT WAS ALREADY SENT
# ============================================================

def alert_already_sent(incident_id):
    """
    Check whether an email alert was already sent
    for the given Incident_ID.
    """

    initialize_alert_history()

    try:

        history_df = pd.read_csv(
            HISTORY_FILE
        )

        if history_df.empty:
            return False

        sent_incidents = history_df[
            history_df["Email_Status"] == "SENT"
        ]["Incident_ID"].astype(str)

        return str(incident_id) in sent_incidents.values

    except Exception as e:

        print(
            f"⚠️ Could not read alert history: {e}"
        )

        return False


# ============================================================
# SAVE ALERT HISTORY
# ============================================================

def save_alert_history(
    incident_id,
    date,
    severity,
    metrics,
    email_status,
    email_id=""
):
    """
    Save email alert information into CSV history.
    """

    initialize_alert_history()

    new_record = pd.DataFrame([
        {
            "Incident_ID": incident_id,
            "Date": date,
            "Severity": severity,
            "Metrics": metrics,
            "Email_Status": email_status,
            "Email_ID": email_id,
            "Sent_At": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    ])

    new_record.to_csv(
        HISTORY_FILE,
        mode="a",
        header=False,
        index=False
    )

    print(
        f"📝 Alert history updated for {incident_id}"
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n📝 Testing alert history system..."
    )

    initialize_alert_history()

    print(
        f"✅ Alert history file ready:"
    )

    print(
        HISTORY_FILE
    )

    test_incident = "INC-TEST"

    if alert_already_sent(test_incident):

        print(
            f"🚫 {test_incident} already exists."
        )

    else:

        save_alert_history(
            incident_id=test_incident,
            date="2026-08-13",
            severity="HIGH",
            metrics="Revenue",
            email_status="SENT",
            email_id="TEST-EMAIL-ID"
        )

        print(
            f"✅ Test alert recorded for {test_incident}"
        )