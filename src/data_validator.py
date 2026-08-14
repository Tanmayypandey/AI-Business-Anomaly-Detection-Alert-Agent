REQUIRED_COLUMNS = [
    "Date",
    "Revenue",
    "Orders",
    "Traffic",
    "Conversion_Rate",
    "Marketing_Cost",
    "Refunds",
    "New_Customers",
    "Returning_Customers"
]


def validate_columns(df):
    missing_columns = []

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:
        print("❌ Data validation failed!")
        print("Missing columns:")

        for column in missing_columns:
            print(f"- {column}")

        return False

    print("✅ All required columns are present.")
    return True