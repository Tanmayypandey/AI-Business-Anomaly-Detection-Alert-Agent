import pandas as pd


MONITORED_METRICS = [
    "Revenue",
    "Orders",
    "Traffic",
    "Conversion_Rate",
    "Marketing_Cost",
    "Refunds"
]


def detect_anomalies(
    df,
    window=7,
    z_threshold=3.0,
    change_threshold=0.20
):

    anomalies = []

    data = df.copy()

    data["Date"] = pd.to_datetime(data["Date"])

    for metric in MONITORED_METRICS:

        # Previous 7 days baseline
        rolling_mean = (
            data[metric]
            .shift(1)
            .rolling(window=window)
            .mean()
        )

        rolling_std = (
            data[metric]
            .shift(1)
            .rolling(window=window)
            .std()
        )

        # Z-score
        z_score = (
            (data[metric] - rolling_mean)
            / rolling_std
        )

        # Percentage difference from baseline
        percentage_change = (
            (data[metric] - rolling_mean)
            / rolling_mean
        )

        # Detection conditions
        statistical_anomaly = (
            z_score.abs() >= z_threshold
        )

        business_anomaly = (
            percentage_change.abs() >= change_threshold
        )

        # A value is anomalous if both conditions are satisfied
        anomaly_mask = (
            statistical_anomaly
            & business_anomaly
        )

        for index in data.index[anomaly_mask]:

            change_percent = (
                percentage_change.loc[index] * 100
            )

            direction = (
                "Increase"
                if change_percent > 0
                else "Decrease"
            )

            anomalies.append({
                "Date": data.loc[index, "Date"],
                "Metric": metric,
                "Value": round(data.loc[index, metric], 2),
                "Baseline": round(rolling_mean.loc[index], 2),
                "Change_%": round(change_percent, 2),
                "Z_Score": round(z_score.loc[index], 2),
                "Direction": direction
            })

    return pd.DataFrame(anomalies)


if __name__ == "__main__":

    file_path = "data/raw/business_data.xlsx"

    df = pd.read_excel(file_path)

    anomaly_df = detect_anomalies(df)

    print("\n🚨 ANOMALY DETECTION RESULTS")
    print("=" * 70)

    if anomaly_df.empty:

        print("No significant anomalies detected.")

    else:

        print(anomaly_df.to_string(index=False))

        print("\n")
        print(f"Total significant anomalies detected: {len(anomaly_df)}")