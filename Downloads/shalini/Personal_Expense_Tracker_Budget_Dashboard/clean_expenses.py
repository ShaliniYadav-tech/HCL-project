"""Clean the generated expense data and quarantine invalid records."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "expenses.csv"
CLEAN = ROOT / "data" / "clean"
QUARANTINE = CLEAN / "quarantine"
CLEAN.mkdir(parents=True, exist_ok=True)
QUARANTINE.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df["category"] = df["category"].fillna("Other").str.strip()
df["description"] = df["description"].fillna("Unspecified")
df["payment_method"] = df["payment_method"].fillna("Unknown")
df["transaction_type"] = df["transaction_type"].fillna("Expense").str.title()

# Preserve a duplicate audit trail before removing repeated transactions.
duplicates = df[df.duplicated(subset=["transaction_id"], keep=False)]
duplicates.to_csv(QUARANTINE / "duplicate_expenses.csv", index=False)
df = df.drop_duplicates(subset=["transaction_id"], keep="first")

invalid = df[
    df["date"].isna()
    | df["amount"].isna()
    | (df["amount"] < 0)
    | (df["transaction_type"] != "Expense")
]
invalid.to_csv(QUARANTINE / "invalid_expenses.csv", index=False)
df = df.drop(invalid.index)

df = df[(df["amount"] > 0) & (df["transaction_type"] == "Expense")].copy()
df["month"] = df["date"].dt.to_period("M").astype(str)
df.to_csv(CLEAN / "expenses.csv", index=False)

print(f"Cleaned {len(df)} expense transactions")
print(f"Quarantined {len(duplicates)} duplicate rows and {len(invalid)} invalid rows")
