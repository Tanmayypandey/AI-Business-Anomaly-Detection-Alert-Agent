import pandas as pd

from src.Anomaly_detector import detect_anomalies
from src.Severity_engine import add_severity
from src.incident_grouper import group_incidents


# ==================================================
# BUSINESS EXPLANATION FUNCTIONS
# ==================================================

def explain_anomaly(row):

    metric = row["Metric"]
    change = row["Change_%"]
    direction = row["Direction"]
    severity = row["Severity"]

    abs_change = abs(change)

    # ----------------------------------------------
    # REVENUE
    # ----------------------------------------------

    if metric == "Revenue":

        if direction == "Increase":

            if abs_change >= 50:
                return (
                    f"Revenue increased by {abs_change:.2f}% "
                    f"compared with the recent baseline. "
                    f"This is a {severity.lower()} deviation and "
                    f"may indicate a sudden increase in demand, "
                    f"successful marketing activity, or a major "
                    f"change in customer purchasing behavior."
                )

            else:
                return (
                    f"Revenue increased by {abs_change:.2f}% "
                    f"compared with the recent baseline. "
                    f"This may indicate stronger demand or "
                    f"improved business performance."
                )

        else:

            return (
                f"Revenue decreased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate reduced demand, lower "
                f"conversion, reduced traffic, or other "
                f"business performance issues."
            )

    # ----------------------------------------------
    # ORDERS
    # ----------------------------------------------

    elif metric == "Orders":

        if direction == "Increase":

            return (
                f"Orders increased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate stronger customer demand "
                f"or successful sales activity."
            )

        else:

            return (
                f"Orders decreased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate weaker demand, reduced "
                f"conversion, or operational issues."
            )

    # ----------------------------------------------
    # TRAFFIC
    # ----------------------------------------------

    elif metric == "Traffic":

        if direction == "Increase":

            return (
                f"Traffic increased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may be related to increased marketing "
                f"activity, campaigns, or external traffic sources."
            )

        else:

            return (
                f"Traffic decreased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate a decline in website visits, "
                f"marketing reach, or traffic acquisition."
            )

    # ----------------------------------------------
    # CONVERSION RATE
    # ----------------------------------------------

    elif metric == "Conversion_Rate":

        if direction == "Increase":

            return (
                f"Conversion rate increased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This suggests that a larger proportion of "
                f"visitors are converting into customers."
            )

        else:

            return (
                f"Conversion rate decreased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate lower traffic quality, "
                f"website or checkout issues, pricing changes, "
                f"or reduced customer intent."
            )

    # ----------------------------------------------
    # MARKETING COST
    # ----------------------------------------------

    elif metric == "Marketing_Cost":

        if direction == "Increase":

            return (
                f"Marketing cost increased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate increased advertising spend "
                f"or an unusually expensive acquisition period."
            )

        else:

            return (
                f"Marketing cost decreased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate reduced advertising activity "
                f"or lower campaign spending."
            )

    # ----------------------------------------------
    # REFUNDS
    # ----------------------------------------------

    elif metric == "Refunds":

        if direction == "Increase":

            return (
                f"Refunds increased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This may indicate product returns, payment "
                f"issues, delivery problems, or customer "
                f"satisfaction concerns."
            )

        else:

            return (
                f"Refunds decreased by {abs_change:.2f}% "
                f"compared with the recent baseline. "
                f"This generally indicates fewer refunds and "
                f"may represent an improvement in customer "
                f"experience or order quality."
            )

    # ----------------------------------------------
    # DEFAULT
    # ----------------------------------------------

    else:

        return (
            f"{metric} changed by {abs_change:.2f}% "
            f"compared with the recent baseline. "
            f"This metric requires further investigation."
        )


# ==================================================
# ADD EXPLANATION COLUMN
# ==================================================

def add_explanations(incident_df):

    if incident_df.empty:
        return incident_df

    result = incident_df.copy()

    result["Business_Explanation"] = result.apply(
        explain_anomaly,
        axis=1
    )

    return result


# ==================================================
# MAIN PROGRAM
# ==================================================

if __name__ == "__main__":

    file_path = "data/raw/business_data.xlsx"

    print("\n📂 Loading business data...")

    # Load Excel
    df = pd.read_excel(file_path)

    print("✅ Excel file loaded successfully!")

    # ----------------------------------------------
    # STEP 1: Detect anomalies
    # ----------------------------------------------

    print("\n🔍 Detecting anomalies...")

    anomaly_df = detect_anomalies(df)

    print(
        f"✅ {len(anomaly_df)} anomalies detected."
    )

    # ----------------------------------------------
    # STEP 2: Add severity
    # ----------------------------------------------

    print("\n⚠️ Calculating severity...")

    severity_df = add_severity(anomaly_df)

    print("✅ Severity calculated.")

    # ----------------------------------------------
    # STEP 3: Group incidents
    # ----------------------------------------------

    print("\n🔗 Grouping incidents...")

    incident_df = group_incidents(
        severity_df
    )

    print("✅ Incident grouping completed.")

    # ----------------------------------------------
    # STEP 4: Generate explanations
    # ----------------------------------------------

    print("\n🧠 Generating business explanations...")

    explained_df = add_explanations(
        incident_df
    )

    print("✅ Business explanations generated.")

    # ----------------------------------------------
    # STEP 5: Display report
    # ----------------------------------------------

    print("\n🚨 BUSINESS ANOMALY REPORT")
    print("=" * 120)

    if explained_df.empty:

        print("No significant anomalies detected.")

    else:

        print(
            explained_df.to_string(
                index=False
            )
        )

        # ------------------------------------------
        # Summary
        # ------------------------------------------

        total_anomalies = len(
            explained_df
        )

        total_incidents = (
            explained_df["Incident_ID"]
            .nunique()
        )

        print("\n")
        print("=" * 60)
        print("📊 BUSINESS SUMMARY")
        print("=" * 60)

        print(
            f"Total anomalies : {total_anomalies}"
        )

        print(
            f"Total incidents : {total_incidents}"
        )

        # ------------------------------------------
        # Severity summary
        # ------------------------------------------

        print("\n📊 SEVERITY SUMMARY")
        print("-" * 50)

        print(
            explained_df["Severity"]
            .value_counts()
        )

        print("\n✅ Business explanation engine completed!")