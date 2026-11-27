"""Generate a reproducible sample expense dataset for project 9."""

from pathlib import Path
import random

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

random.seed(9)

categories = {
    "Housing": (5000, 12000),
    "Food": (150, 900),
    "Transport": (100, 1200),
    "Utilities": (700, 3500),
    "Health": (200, 2500),
    "Shopping": (300, 4500),
    "Entertainment": (200, 1800),
    "Education": (300, 3000),
    "Travel": (1500, 9000),
    "Savings": (1000, 5000),
}
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Bank Transfer"]

rows = []
transaction_id = 1
for year in (2025, 2026):
    for month in range(1, 13):
        for category, (low, high) in categories.items():
            count = 1 if category in {"Housing", "Utilities", "Savings"} else random.randint(2, 5)
            for _ in range(count):
                day = random.randint(1, 28)
                amount = round(random.uniform(low, high), 2)
                if category == "Housing":
                    amount = 10000
                rows.append({
                    "transaction_id": f"E{transaction_id:05d}",
                    "date": f"{year}-{month:02d}-{day:02d}",
                    "category": category,
                    "description": f"{category} expense",
                    "amount": amount,
                    "transaction_type": "Expense",
                    "payment_method": random.choice(payment_methods),
                })
                transaction_id += 1

df = pd.DataFrame(rows)

# Deliberate test cases: duplicates, missing category, negative amount and transfer.
df = pd.concat([df, df.iloc[[5, 42, 91]].copy()], ignore_index=True)
df.loc[42, "category"] = None
df.loc[91, "amount"] = -450
df.loc[120, "transaction_type"] = "Transfer"

df.to_csv(RAW / "expenses.csv", index=False)
print(f"Generated {len(df)} raw transactions in {RAW / 'expenses.csv'}")
