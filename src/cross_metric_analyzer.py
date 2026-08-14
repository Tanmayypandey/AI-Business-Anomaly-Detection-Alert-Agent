import pandas as pd

from src.Anomaly_detector import detect_anomalies
from src.Severity_engine import add_severity
from src.incident_grouper import group_incidents
from src.business_explainer import add_explanations


# ==================================================
# CROSS-METRIC BUSINESS REASONING
# ==================================================

def analyze_incident(metrics_df):

    """
    Analyze multiple anomalies belonging to one incident
    and generate a business-level insight + recommendation.
    """

    if metrics_df.empty:
        return (
            "No business insight available.",
            "No action required."
        )

    metrics = metrics_df["Metric"].tolist()

    # Convert metrics into a quick lookup dictionary
    metric_data = {}

    for _, row in metrics_df.iterrows():

        metric_data[row["Metric"]] = {
            "change": row["Change_%"],
            "direction": row["Direction"],
            "severity": row["Severity"]
        }

    # ==================================================
    # RULE 1: REVENUE + ORDERS
    # ==================================================

    if "Revenue" in metric_data and "Orders" in metric_data:

        revenue = metric_data["Revenue"]
        orders = metric_data["Orders"]

        if (
            revenue["direction"] == "Increase"
            and orders["direction"] == "Increase"
        ):

            insight = (
                f"Revenue and orders increased together. "
                f"Revenue changed by {abs(revenue['change']):.2f}% "
                f"and orders changed by {abs(orders['change']):.2f}%. "
                f"This indicates unusually strong sales activity "
                f"during this period."
            )

            action = (
                "Investigate which products, campaigns, customer "
                "segments, or sales channels contributed to the increase "
                "and determine whether the growth can be sustained."
            )

            return insight, action

        elif (
            revenue["direction"] == "Decrease"
            and orders["direction"] == "Decrease"
        ):

            insight = (
                f"Revenue and orders decreased together. "
                f"Revenue changed by {revenue['change']:.2f}% "
                f"and orders changed by {orders['change']:.2f}%. "
                f"This indicates a potential decline in sales demand."
            )

            action = (
                "Investigate customer demand, product availability, "
                "pricing, marketing performance, and conversion issues."
            )

            return insight, action

        elif (
            revenue["direction"] == "Increase"
            and orders["direction"] == "Decrease"
        ):

            insight = (
                "Revenue increased while orders decreased. "
                "This may indicate that the average order value increased "
                "significantly despite fewer orders."
            )

            action = (
                "Investigate changes in product mix, pricing, discounts, "
                "and average order value."
            )

            return insight, action

        elif (
            revenue["direction"] == "Decrease"
            and orders["direction"] == "Increase"
        ):

            insight = (
                "Orders increased while revenue decreased. "
                "This may indicate that customers are placing more orders "
                "with lower average order values."
            )

            action = (
                "Investigate product mix, pricing, discounts, and "
                "average order value."
            )

            return insight, action

    # ==================================================
    # RULE 2: TRAFFIC + CONVERSION RATE
    # ==================================================

    if "Traffic" in metric_data and "Conversion_Rate" in metric_data:

        traffic = metric_data["Traffic"]
        conversion = metric_data["Conversion_Rate"]

        if (
            traffic["direction"] == "Increase"
            and conversion["direction"] == "Decrease"
        ):

            insight = (
                f"Traffic increased by {abs(traffic['change']):.2f}% "
                f"while conversion rate decreased by "
                f"{abs(conversion['change']):.2f}%. "
                f"This suggests that additional traffic may not be "
                f"converting effectively."
            )

            action = (
                "Investigate traffic sources, landing pages, audience "
                "quality, website performance, and the customer journey."
            )

            return insight, action

        elif (
            traffic["direction"] == "Decrease"
            and conversion["direction"] == "Increase"
        ):

            insight = (
                f"Traffic decreased by {abs(traffic['change']):.2f}% "
                f"while conversion rate increased by "
                f"{abs(conversion['change']):.2f}%. "
                f"This suggests lower traffic volume but potentially "
                f"higher-quality visitors."
            )

            action = (
                "Identify which traffic sources declined and determine "
                "whether the remaining sources are producing higher-value "
                "customers."
            )

            return insight, action

        elif (
            traffic["direction"] == "Increase"
            and conversion["direction"] == "Increase"
        ):

            insight = (
                f"Traffic increased by {abs(traffic['change']):.2f}% "
                f"and conversion rate also increased by "
                f"{abs(conversion['change']):.2f}%. "
                f"This indicates strong acquisition and conversion "
                f"performance."
            )

            action = (
                "Identify the campaigns and traffic sources responsible "
                "for the improvement and consider scaling them."
            )

            return insight, action

        elif (
            traffic["direction"] == "Decrease"
            and conversion["direction"] == "Decrease"
        ):

            insight = (
                f"Both traffic and conversion rate decreased. "
                f"Traffic changed by {traffic['change']:.2f}% and "
                f"conversion rate changed by {conversion['change']:.2f}%. "
                f"This indicates a potentially broad decline in "
                f"customer acquisition and conversion performance."
            )

            action = (
                "Investigate marketing channels, website performance, "
                "landing pages, customer demand, and technical issues."
            )

            return insight, action

    # ==================================================
    # RULE 3: TRAFFIC + MARKETING COST
    # ==================================================

    if "Traffic" in metric_data and "Marketing_Cost" in metric_data:

        traffic = metric_data["Traffic"]
        marketing = metric_data["Marketing_Cost"]

        if (
            marketing["direction"] == "Increase"
            and traffic["direction"] == "Decrease"
        ):

            insight = (
                f"Marketing cost increased by "
                f"{abs(marketing['change']):.2f}% while traffic "
                f"decreased by {abs(traffic['change']):.2f}%. "
                f"This suggests a possible decline in marketing efficiency."
            )

            action = (
                "Review campaign performance, acquisition costs, "
                "advertising channels, targeting, and budget allocation."
            )

            return insight, action

        elif (
            marketing["direction"] == "Decrease"
            and traffic["direction"] == "Increase"
        ):

            insight = (
                f"Marketing cost decreased by "
                f"{abs(marketing['change']):.2f}% while traffic "
                f"increased by {abs(traffic['change']):.2f}%. "
                f"This may indicate improved marketing efficiency."
            )

            action = (
                "Identify the channels responsible for the traffic growth "
                "and evaluate whether spending can be optimized further."
            )

            return insight, action

        elif (
            marketing["direction"] == "Increase"
            and traffic["direction"] == "Increase"
        ):

            insight = (
                f"Marketing cost and traffic both increased. "
                f"Marketing cost changed by "
                f"{abs(marketing['change']):.2f}% while traffic changed by "
                f"{abs(traffic['change']):.2f}%. "
                f"This may indicate that increased spending generated "
                f"additional traffic."
            )

            action = (
                "Compare the additional traffic against acquisition cost "
                "and conversion performance to evaluate campaign ROI."
            )

            return insight, action

    # ==================================================
    # RULE 4: REVENUE + REFUNDS
    # ==================================================

    if "Revenue" in metric_data and "Refunds" in metric_data:

        revenue = metric_data["Revenue"]
        refunds = metric_data["Refunds"]

        if (
            revenue["direction"] == "Increase"
            and refunds["direction"] == "Increase"
        ):

            insight = (
                f"Revenue increased by {abs(revenue['change']):.2f}% "
                f"while refunds also increased by "
                f"{abs(refunds['change']):.2f}%. "
                f"This indicates that sales growth may be accompanied "
                f"by increased refund activity."
            )

            action = (
                "Investigate refunded orders, products with high return "
                "rates, payment issues, delivery problems, and customer "
                "complaints."
            )

            return insight, action

        elif (
            revenue["direction"] == "Decrease"
            and refunds["direction"] == "Increase"
        ):

            insight = (
                f"Revenue decreased by {abs(revenue['change']):.2f}% "
                f"while refunds increased by "
                f"{abs(refunds['change']):.2f}%. "
                f"This combination may indicate a significant business "
                f"performance or customer satisfaction problem."
            )

            action = (
                "Immediately investigate refunded transactions, product "
                "quality, delivery issues, payment problems, and customer "
                "complaints."
            )

            return insight, action

    # ==================================================
    # RULE 5: ORDERS + REFUNDS
    # ==================================================

    if "Orders" in metric_data and "Refunds" in metric_data:

        orders = metric_data["Orders"]
        refunds = metric_data["Refunds"]

        if (
            orders["direction"] == "Increase"
            and refunds["direction"] == "Increase"
        ):

            insight = (
                f"Orders increased by {abs(orders['change']):.2f}% "
                f"while refunds increased by "
                f"{abs(refunds['change']):.2f}%. "
                f"This may indicate that higher sales volume is "
                f"accompanied by increased return or refund activity."
            )

            action = (
                "Identify products or customer segments contributing "
                "to refunds and investigate order quality."
            )

            return insight, action

    # ==================================================
    # RULE 6: MARKETING COST + CONVERSION RATE
    # ==================================================

    if (
        "Marketing_Cost" in metric_data
        and "Conversion_Rate" in metric_data
    ):

        marketing = metric_data["Marketing_Cost"]
        conversion = metric_data["Conversion_Rate"]

        if (
            marketing["direction"] == "Increase"
            and conversion["direction"] == "Decrease"
        ):

            insight = (
                f"Marketing cost increased by "
                f"{abs(marketing['change']):.2f}% while conversion rate "
                f"decreased by {abs(conversion['change']):.2f}%. "
                f"This may indicate declining marketing efficiency."
            )

            action = (
                "Review campaign targeting, customer acquisition cost, "
                "landing pages, and conversion funnel performance."
            )

            return insight, action

    # ==================================================
    # DEFAULT CASE
    # ==================================================

    # If only one metric exists or no specific combination
    # was detected.

    row = metrics_df.iloc[0]

    insight = (
        f"The {row['Metric']} metric changed by "
        f"{abs(row['Change_%']):.2f}% compared with its recent "
        f"baseline. The anomaly requires further investigation."
    )

    action = (
        f"Review the underlying {row['Metric']} data, identify the "
        f"source of the change, and compare it with related business "
        f"metrics."
    )

    return insight, action


# ==================================================
# ANALYZE ALL INCIDENTS
# ==================================================

def add_cross_metric_analysis(incident_df):

    if incident_df.empty:
        return incident_df

    result = incident_df.copy()

    insights = {}
    actions = {}

    # Analyze each incident separately
    for incident_id, group in result.groupby("Incident_ID"):

        insight, action = analyze_incident(group)

        insights[incident_id] = insight
        actions[incident_id] = action

    # Add results to dataframe
    result["Business_Insight"] = (
        result["Incident_ID"]
        .map(insights)
    )

    result["Recommended_Action"] = (
        result["Incident_ID"]
        .map(actions)
    )

    return result


# ==================================================
# MAIN PROGRAM
# ==================================================

if __name__ == "__main__":

    file_path = "data/raw/business_data.xlsx"

    print("\n📂 Loading business data...")

    # ----------------------------------------------
    # Load Excel
    # ----------------------------------------------

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
    # STEP 4: Add individual explanations
    # ----------------------------------------------

    print("\n🧠 Generating metric explanations...")

    explained_df = add_explanations(
        incident_df
    )

    print("✅ Metric explanations generated.")

    # ----------------------------------------------
    # STEP 5: Cross-metric analysis
    # ----------------------------------------------

    print("\n🤖 Performing cross-metric business reasoning...")

    final_df = add_cross_metric_analysis(
        explained_df
    )

    print(
        "✅ Cross-metric reasoning completed."
    )

    # ----------------------------------------------
    # STEP 6: Display report
    # ----------------------------------------------

    print("\n🚨 BUSINESS INTELLIGENCE REPORT")
    print("=" * 140)

    if final_df.empty:

        print("No significant anomalies detected.")

    else:

        # Display selected columns
        display_columns = [
            "Incident_ID",
            "Date",
            "Metric",
            "Change_%",
            "Direction",
            "Severity",
            "Business_Insight",
            "Recommended_Action"
        ]

        print(
            final_df[display_columns]
            .to_string(index=False)
        )

        # ------------------------------------------
        # Summary
        # ------------------------------------------

        total_anomalies = len(
            final_df
        )

        total_incidents = (
            final_df["Incident_ID"]
            .nunique()
        )

        print("\n")
        print("=" * 70)
        print("📊 BUSINESS INTELLIGENCE SUMMARY")
        print("=" * 70)

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
            final_df["Severity"]
            .value_counts()
        )

        print(
            "\n✅ Cross-metric business analysis completed!"
        )