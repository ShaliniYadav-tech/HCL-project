"""Create KPIs, budget breaches and charts for the expense dashboard."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "clean" / "expenses.csv"
REPORTS = ROOT / "reports"
CHARTS = REPORTS / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

budgets = {
    "Housing": 12000, "Food": 5000, "Transport": 3500, "Utilities": 4000,
    "Health": 3000, "Shopping": 7000, "Entertainment": 3500,
    "Education": 5000, "Travel": 9000, "Savings": 5000, "Other": 1000,
}

df = pd.read_csv(DATA)
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)
df["budget"] = df["category"].map(budgets).fillna(1000)

monthly = df.groupby(["month", "category"], as_index=False)["amount"].sum()
monthly_budget = monthly.copy()
monthly_budget["budget"] = monthly_budget["category"].map(budgets).fillna(1000)
monthly_budget["breach"] = monthly_budget["amount"] > monthly_budget["budget"]

breaches = monthly_budget[monthly_budget["breach"]].copy()
breaches["over_by"] = breaches["amount"] - breaches["budget"]

category_totals = df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
monthly_totals = df.groupby("month", as_index=False)["amount"].sum()

kpis = {
    "total_expenses": round(float(df["amount"].sum()), 2),
    "average_monthly_expense": round(float(monthly_totals["amount"].mean()), 2),
    "highest_spending_category": category_totals.iloc[0]["category"],
    "highest_category_amount": round(float(category_totals.iloc[0]["amount"]), 2),
    "budget_breach_count": int(len(breaches)),
    "total_over_budget": round(float(breaches["over_by"].sum()), 2),
    "transaction_count": int(len(df)),
    "date_range": [df["date"].min().strftime("%Y-%m-%d"), df["date"].max().strftime("%Y-%m-%d")],
}
(REPORTS / "kpis.json").write_text(json.dumps(kpis, indent=2), encoding="utf-8")
breaches.to_csv(REPORTS / "budget_breaches.csv", index=False)
category_totals.to_csv(REPORTS / "category_totals.csv", index=False)
monthly_totals.to_csv(REPORTS / "monthly_totals.csv", index=False)

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_totals["month"], monthly_totals["amount"], marker="o", color="#2563eb")
ax.set_title("Monthly Expense Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Expense (INR)")
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / "01_monthly_expense_trend.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(category_totals["category"], category_totals["amount"], color="#4f46e5")
ax.invert_yaxis()
ax.set_title("Total Expense by Category")
ax.set_xlabel("Expense (INR)")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(CHARTS / "02_category_totals.png", dpi=150)
plt.close(fig)

print(json.dumps(kpis, indent=2))
