import os
import pandas as pd
from datetime import datetime

from src.ai_explainer import analyze_incident_with_ai
from src.Anomaly_detector import detect_anomalies
from src.Severity_engine import add_severity
from src.incident_grouper import group_incidents
from src.email_alert import send_alert_email

from src.alert_history import (
    alert_already_sent,
    save_alert_history
)


# ============================================================
# SEVERITY PRIORITY
# ============================================================

SEVERITY_PRIORITY = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}


# ============================================================
# GET HIGHEST SEVERITY OF INCIDENT
# ============================================================

def get_incident_severity(group):

    severities = (
        group["Severity"]
        .astype(str)
        .str.upper()
    )

    highest_severity = max(
        severities,
        key=lambda x: SEVERITY_PRIORITY.get(x, 0)
    )

    return highest_severity


# ============================================================
# GENERATE AI BUSINESS REPORT
# ============================================================

def generate_ai_report(incident_df):

    if incident_df.empty:
        return "No significant incidents detected."

    reports = []

    total_incidents = (
        incident_df["Incident_ID"]
        .nunique()
    )

    print(
        f"\n📊 Total incidents to analyze: "
        f"{total_incidents}"
    )

    # --------------------------------------------------------
    # Analyze every incident
    # --------------------------------------------------------

    for number, (incident_id, group) in enumerate(
        incident_df.groupby("Incident_ID"),
        start=1
    ):

        print(
            f"\n🤖 [{number}/{total_incidents}] "
            f"Analyzing {incident_id} with Llama 3.2..."
        )

        try:

            # ------------------------------------------------
            # AI ANALYSIS
            # ------------------------------------------------

            ai_response = analyze_incident_with_ai(
                group
            )

            # ------------------------------------------------
            # Incident information
            # ------------------------------------------------

            incident_date = group["Date"].iloc[0]

            if hasattr(
                incident_date,
                "strftime"
            ):

                incident_date = incident_date.strftime(
                    "%Y-%m-%d"
                )

            metrics = ", ".join(
                group["Metric"]
                .astype(str)
                .unique()
                .tolist()
            )

            # ------------------------------------------------
            # Get highest severity
            # ------------------------------------------------

            severity = get_incident_severity(
                group
            )

            # ------------------------------------------------
            # Build report
            # ------------------------------------------------

            report = f"""
============================================================
INCIDENT: {incident_id}
DATE: {incident_date}
METRICS: {metrics}
SEVERITY: {severity}
============================================================

{ai_response}

"""

            reports.append(report)

            print(
                f"✅ {incident_id} analysis completed."
            )

            # =================================================
            # AUTOMATIC EMAIL ALERT
            # WITH DUPLICATE PROTECTION
            # =================================================

            if severity in ["HIGH", "CRITICAL"]:

                print(
                    f"\n📧 {severity} severity detected!"
                )

                # ------------------------------------------------
                # Check alert history
                # ------------------------------------------------

                if alert_already_sent(
                    incident_id
                ):

                    print(
                        f"🚫 Email already sent for "
                        f"{incident_id}."
                    )

                    print(
                        "⏭️ Skipping duplicate alert."
                    )

                else:

                    print(
                        f"🚀 Sending email alert for "
                        f"{incident_id}..."
                    )

                    email_sent = send_alert_email(

                        incident_id=incident_id,

                        incident_date=incident_date,

                        metrics=metrics,

                        severity=severity,

                        ai_analysis=ai_response
                    )

                    # ------------------------------------------------
                    # Email successful
                    # ------------------------------------------------

                    if email_sent:

                        print(
                            f"✅ Email alert sent for "
                            f"{incident_id}!"
                        )

                        # Save email history
                        save_alert_history(

                            incident_id=incident_id,

                            date=incident_date,

                            severity=severity,

                            metrics=metrics,

                            email_status="SENT",

                            email_id=str(email_sent)
                        )

                    # ------------------------------------------------
                    # Email failed
                    # ------------------------------------------------

                    else:

                        print(
                            f"❌ Email alert failed for "
                            f"{incident_id}."
                        )

            # ------------------------------------------------
            # LOW / MEDIUM
            # ------------------------------------------------

            else:

                print(
                    f"ℹ️ {incident_id} is "
                    f"{severity} severity."
                )

                print(
                    "📧 Email alert not required."
                )

        # =====================================================
        # INCIDENT ERROR HANDLING
        # =====================================================

        except Exception as e:

            print(
                f"❌ {incident_id} analysis failed: "
                f"{e}"
            )

            reports.append(
                f"""
============================================================
INCIDENT: {incident_id}
============================================================

❌ AI analysis failed:

{e}

"""
            )

    return "\n".join(reports)


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    print(
        "\n📂 Loading business data..."
    )

    file_path = (
        "data/raw/business_data.xlsx"
    )

    # --------------------------------------------------------
    # Load Excel
    # --------------------------------------------------------

    df = pd.read_excel(
        file_path
    )

    print(
        "✅ Excel file loaded successfully!"
    )

    # --------------------------------------------------------
    # STEP 1: Detect anomalies
    # --------------------------------------------------------

    print(
        "\n🔍 Detecting anomalies..."
    )

    anomaly_df = detect_anomalies(
        df
    )

    print(
        f"✅ {len(anomaly_df)} anomalies detected."
    )

    # --------------------------------------------------------
    # STEP 2: Calculate severity
    # --------------------------------------------------------

    print(
        "\n⚠️ Calculating severity..."
    )

    severity_df = add_severity(
        anomaly_df
    )

    print(
        "✅ Severity calculated."
    )

    # --------------------------------------------------------
    # STEP 3: Group incidents
    # --------------------------------------------------------

    print(
        "\n🔗 Grouping incidents..."
    )

    incident_df = group_incidents(
        severity_df
    )

    print(
        "✅ Incident grouping completed."
    )

    # --------------------------------------------------------
    # STEP 4: Generate AI report
    # --------------------------------------------------------

    if incident_df.empty:

        print(
            "\n❌ No incidents found."
        )

    else:

        total_incidents = (
            incident_df["Incident_ID"]
            .nunique()
        )

        print(
            f"\n📊 Total incidents found: "
            f"{total_incidents}"
        )

        print(
            "\n🚀 Starting full AI business "
            "analysis + automatic alerts..."
        )

        # ----------------------------------------------------
        # Generate AI report
        # ----------------------------------------------------

        ai_report = generate_ai_report(
            incident_df
        )

        # ----------------------------------------------------
        # STEP 5: Save report
        # ----------------------------------------------------

        report_folder = "reports"

        os.makedirs(
            report_folder,
            exist_ok=True
        )

        report_file = (
            f"{report_folder}/AI_Business_Report_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        with open(
            report_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "=" * 70 + "\n"
            )

            file.write(
                "🤖 AI BUSINESS ANOMALY REPORT\n"
            )

            file.write(
                "=" * 70 + "\n\n"
            )

            file.write(
                f"Generated: "
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

            file.write(
                f"Total Anomalies: "
                f"{len(anomaly_df)}\n"
            )

            file.write(
                f"Total Incidents: "
                f"{total_incidents}\n\n"
            )

            file.write(
                "=" * 70 + "\n\n"
            )

            file.write(
                ai_report
            )

            file.write(
                "\n\n"
                + "=" * 70
                + "\n"
            )

        # ----------------------------------------------------
        # FINAL OUTPUT
        # ----------------------------------------------------

        print("\n")

        print(
            "=" * 70
        )

        print(
            "🎉 AI BUSINESS ANALYSIS + ALERTS COMPLETED"
        )

        print(
            "=" * 70
        )

        print(
            f"\n📊 Total anomalies : "
            f"{len(anomaly_df)}"
        )

        print(
            f"📊 Total incidents : "
            f"{total_incidents}"
        )

        print(
            "\n📄 Complete report saved at:"
        )

        print(
            report_file
        )

        print(
            "\n📧 Alert Rules:"
        )

        print(
            "🟢 LOW      → No email"
        )

        print(
            "🟡 MEDIUM   → No email"
        )

        print(
            "🔴 HIGH     → Email alert"
        )

        print(
            "🚨 CRITICAL → Email alert"
        )

        print(
            "\n🛡️ Duplicate protection:"
        )

        print(
            "HIGH/CRITICAL alerts are checked "
            "against alert history before sending."
        )

        print(
            "\n✅ Automatic alert system completed!"
        )