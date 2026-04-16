import os
import pandas as pd
import numpy as np

# -----------------------------
# CREATE FOLDERS
# -----------------------------
os.makedirs("data", exist_ok=True)

# -----------------------------
# GENERATE SYNTHETIC DATA
# -----------------------------
def generate_data(num_records=300):
    np.random.seed(42)

    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")

    categories = ["Food", "Rent", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Education"]
    payment_methods = ["Cash", "UPI", "Card", "Net Banking"]

    data = {
        "date": np.random.choice(dates, num_records),
        "category": np.random.choice(categories, num_records),
        "amount": np.random.randint(100, 10000, num_records),
        "payment_method": np.random.choice(payment_methods, num_records)
    }

    df = pd.DataFrame(data)

    # Adjust realistic spending
    df.loc[df["category"] == "Rent", "amount"] = np.random.randint(5000, 20000, df[df["category"] == "Rent"].shape[0])
    df.loc[df["category"] == "Bills", "amount"] = np.random.randint(1000, 8000, df[df["category"] == "Bills"].shape[0])

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    return df


# -----------------------------
# SAVE DATA
# -----------------------------
if __name__ == "__main__":
    df = generate_data(300)
    df.to_csv("data/expenses.csv", index=False)
    print("✅ Data generated and saved to data/expenses.csv")