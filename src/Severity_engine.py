import pandas as pd

# Import anomaly detector from src package
from src.Anomaly_detector import detect_anomalies


# ==================================================
# SEVERITY CALCULATION
# ==================================================

def calculate_severity(change_percent, z_score):

    change = abs(change_percent)
    z = abs(z_score)

    # CRITICAL
    if change >= 50 or z >= 5:
        return "CRITICAL"

    # HIGH
    elif change >= 40 or z >= 4:
        return "HIGH"

    # MEDIUM
    elif change >= 30 or z >= 3:
        return "MEDIUM"

    # LOW
    else:
        return "LOW"


# ==================================================
# ADD SEVERITY TO ANOMALIES
# ==================================================

def add_severity(anomaly_df):

    # If no anomalies are detected
    if anomaly_df.empty:
        return anomaly_df

    result = anomaly_df.copy()

    result["Severity"] = result.apply(
        lambda row: calculate_severity(
            row["Change_%"],
            row["Z_Score"]
        ),
        axis=1
    )

    return result


# ==================================================
# MAIN PROGRAM
# ==================================================

if __name__ == "__main__":

    # Excel file path
    file_path = "data/raw/business_data.xlsx"

    print("\n📂 Loading business data...")

    # Load Excel
    df = pd.read_excel(file_path)

    print("✅ Excel file loaded successfully!")

    # ----------------------------------------------
    # STEP 1: Detect anomalies using 5.2 detector
    # ----------------------------------------------

    print("\n🔍 Running anomaly detection...")

    anomaly_df = detect_anomalies(df)

    print(
        f"✅ Anomaly detection completed!"
    )

    # ----------------------------------------------
    # STEP 2: Add severity
    # ----------------------------------------------

    result = add_severity(anomaly_df)

    # ----------------------------------------------
    # STEP 3: Display results
    # ----------------------------------------------

    print("\n🚨 ANOMALY REPORT WITH SEVERITY")
    print("=" * 100)

    if result.empty:

        print("No significant anomalies detected.")

    else:

        print(
            result.to_string(
                index=False
            )
        )

        # ------------------------------------------
        # Total anomalies
        # ------------------------------------------

        print("\n")
        print(
            f"Total significant anomalies detected: "
            f"{len(result)}"
        )

        # ------------------------------------------
        # Severity summary
        # ------------------------------------------

        print("\n📊 SEVERITY SUMMARY")
        print("-" * 50)

        severity_summary = (
            result["Severity"]
            .value_counts()
        )

        print(severity_summary)

        # ------------------------------------------
        # Critical alerts
        # ------------------------------------------

        critical_count = (
            (result["Severity"] == "CRITICAL")
            .sum()
        )

        high_count = (
            (result["Severity"] == "HIGH")
            .sum()
        )

        print("\n🚨 ALERT SUMMARY")
        print("-" * 50)

        print(f"Critical Alerts : {critical_count}")
        print(f"High Alerts     : {high_count}")

        print("\n✅ Severity analysis completed!")