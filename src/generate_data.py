import pandas as pd
import numpy as np

# Reproducible data
np.random.seed(42)

# 365 days
dates = pd.date_range(
    start="2025-08-01",
    end="2026-07-31",
    freq="D"
)

data = []

for date in dates:

    # Basic business metrics
    traffic = np.random.randint(15000, 25000)

    conversion_rate = np.random.uniform(5.5, 8.0)

    orders = int(traffic * conversion_rate / 100)

    average_order_value = np.random.uniform(900, 1300)

    revenue = orders * average_order_value

    marketing_cost = np.random.uniform(20000, 40000)

    refunds = revenue * np.random.uniform(0.02, 0.06)

    new_customers = int(orders * np.random.uniform(0.50, 0.65))

    returning_customers = orders - new_customers

    data.append({
        "Date": date,
        "Revenue": round(revenue, 2),
        "Orders": orders,
        "Traffic": traffic,
        "Conversion_Rate": round(conversion_rate, 2),
        "Marketing_Cost": round(marketing_cost, 2),
        "Refunds": round(refunds, 2),
        "New_Customers": new_customers,
        "Returning_Customers": returning_customers
    })


# Create DataFrame
df = pd.DataFrame(data)


# --------------------------------------------------
# INTENTIONAL ANOMALIES
# --------------------------------------------------

# 1. Traffic spike + conversion/revenue drop
mask = df["Date"] == pd.Timestamp("2025-10-15")

df.loc[mask, "Traffic"] = (
    df.loc[mask, "Traffic"] * 1.30
).round().astype(int)

df.loc[mask, "Conversion_Rate"] = (
    df.loc[mask, "Conversion_Rate"] * 0.55
).round(2)

df.loc[mask, "Orders"] = (
    df.loc[mask, "Traffic"]
    * df.loc[mask, "Conversion_Rate"]
    / 100
).round().astype(int)

df.loc[mask, "Revenue"] = (
    df.loc[mask, "Revenue"] * 0.70
).round(2)


# 2. Refund spike
mask = df["Date"] == pd.Timestamp("2026-01-20")

df.loc[mask, "Refunds"] = (
    df.loc[mask, "Refunds"] * 4
).round(2)


# 3. Revenue + Orders crash
mask = df["Date"] == pd.Timestamp("2026-03-10")

df.loc[mask, "Revenue"] = (
    df.loc[mask, "Revenue"] * 0.55
).round(2)

df.loc[mask, "Orders"] = (
    df.loc[mask, "Orders"] * 0.60
).round().astype(int)

df.loc[mask, "Conversion_Rate"] = (
    df.loc[mask, "Conversion_Rate"] * 0.65
).round(2)


# 4. Traffic spike + poor conversion
mask = df["Date"] == pd.Timestamp("2026-05-05")

df.loc[mask, "Traffic"] = (
    df.loc[mask, "Traffic"] * 1.60
).round().astype(int)

df.loc[mask, "Conversion_Rate"] = (
    df.loc[mask, "Conversion_Rate"] * 0.60
).round(2)


# --------------------------------------------------
# SAVE TO EXCEL
# --------------------------------------------------

output_path = "data/raw/business_data.xlsx"

df.to_excel(
    output_path,
    index=False
)

print("✅ Business dataset created successfully!")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Saved to: {output_path}")