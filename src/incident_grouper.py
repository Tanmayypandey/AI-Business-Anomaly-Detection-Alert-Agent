import pandas as pd

from src.Anomaly_detector import detect_anomalies
from src.Severity_engine import add_severity


# ==================================================
# GROUP ANOMALIES INTO BUSINESS INCIDENTS
# ==================================================

def group_incidents(anomaly_df):
    """
    Group anomalies occurring on the same date
    into a single business incident.
    """

    if anomaly_df.empty:
        return anomaly_df

    result = anomaly_df.copy()

    # ----------------------------------------------
    # Make sure Date is datetime
    # ----------------------------------------------

    result["Date"] = pd.to_datetime(
        result["Date"]
    )

    # ----------------------------------------------
    # Sort by date and severity
    # ----------------------------------------------

    result = result.sort_values(
        by=["Date", "Severity"],
        ascending=[True, True]
    )

    # ----------------------------------------------
    # Create Incident IDs
    #
    # All anomalies occurring on the same date
    # belong to the same incident.
    # ----------------------------------------------

    unique_dates = (
        result["Date"]
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )

    incident_map = {
        date: f"INC-{index + 1:03d}"
        for index, date in enumerate(unique_dates)
    }

    result["Incident_ID"] = result["Date"].map(
        incident_map
    )

    # ----------------------------------------------
    # Reorder columns
    # ----------------------------------------------

    columns = [
        "Incident_ID",
        "Date",
        "Metric",
        "Value",
        "Baseline",
        "Change_%",
        "Z_Score",
        "Direction",
        "Severity"
    ]

    result = result[columns]

    return result


# ==================================================
# TEST INCIDENT GROUPING
# ==================================================

if __name__ == "__main__":

    file_path = "data/raw/business_data.xlsx"

    print("\n📂 Loading business data...")

    df = pd.read_excel(file_path)

    print("✅ Excel file loaded successfully!")

    # ----------------------------------------------
    # Detect anomalies
    # ----------------------------------------------

    print("\n🔍 Detecting anomalies...")

    anomaly_df = detect_anomalies(df)

    print(
        f"✅ {len(anomaly_df)} anomalies detected."
    )

    # ----------------------------------------------
    # Calculate severity
    # ----------------------------------------------

    print("\n⚠️ Calculating severity...")

    severity_df = add_severity(
        anomaly_df
    )

    print("✅ Severity calculated.")

    # ----------------------------------------------
    # Group incidents
    # ----------------------------------------------

    print("\n🔗 Grouping incidents...")

    incident_df = group_incidents(
        severity_df
    )

    print("✅ Incident grouping completed.")

    # ----------------------------------------------
    # Display result
    # ----------------------------------------------

    print("\n🚨 BUSINESS INCIDENT REPORT")
    print("=" * 100)

    if incident_df.empty:

        print("No incidents detected.")

    else:

        print(
            incident_df.to_string(
                index=False
            )
        )

        # ------------------------------------------
        # Summary
        # ------------------------------------------

        total_anomalies = len(
            incident_df
        )

        total_incidents = (
            incident_df["Incident_ID"]
            .nunique()
        )

        print("\n")
        print("=" * 60)
        print("📊 INCIDENT SUMMARY")
        print("=" * 60)

        print(
            f"Total anomalies : "
            f"{total_anomalies}"
        )

        print(
            f"Total incidents : "
            f"{total_incidents}"
        )

        # ------------------------------------------
        # Anomalies per incident
        # ------------------------------------------

        print(
            "\n📌 ANOMALIES PER INCIDENT"
        )

        print("-" * 50)

        incident_counts = (
            incident_df["Incident_ID"]
            .value_counts()
            .sort_index()
        )

        print(incident_counts)

        # ------------------------------------------
        # Severity summary
        # ------------------------------------------

        print(
            "\n📊 SEVERITY SUMMARY"
        )

        print("-" * 50)

        print(
            incident_df["Severity"]
            .value_counts()
        )

        print(
            "\n✅ Incident analysis completed!"
        )