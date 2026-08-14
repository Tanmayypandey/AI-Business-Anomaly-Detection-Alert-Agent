import pandas as pd

from data_validator import validate_columns


FILE_PATH = "data/raw/business_data.xlsx"


def load_business_data():

    df = pd.read_excel(FILE_PATH)

    print("Excel file successfully loaded!")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    if not validate_columns(df):
        return None

    return df


if __name__ == "__main__":
    load_business_data()