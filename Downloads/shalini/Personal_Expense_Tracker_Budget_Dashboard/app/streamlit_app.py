"""Interactive Personal Expense Tracker and Budget Dashboard."""

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Expense Tracker & Budget Dashboard", page_icon="₹", layout="wide")

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean" / "expenses.csv"
budgets = {
    "Housing": 12000, "Food": 5000, "Transport": 3500, "Utilities": 4000,
    "Health": 3000, "Shopping": 7000, "Entertainment": 3500,
    "Education": 5000, "Travel": 9000, "Savings": 5000, "Other": 1000,
}

if not CLEAN.exists():
    st.error("Run generate_expenses.py and clean_expenses.py before starting this dashboard.")
    st.stop()

@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["budget"] = df["category"].map(budgets).fillna(1000)
    return df

df = load_data()

st.sidebar.header("Filters")
years = st.sidebar.multiselect("Year", sorted(df["date"].dt.year.unique(), reverse=True),
                               default=sorted(df["date"].dt.year.unique(), reverse=True))
categories = st.sidebar.multiselect("Category", sorted(df["category"].unique()),
                                    default=sorted(df["category"].unique()))
view = df[df["date"].dt.year.isin(years) & df["category"].isin(categories)]

st.title("Personal Expense Tracker")
st.caption("Track monthly spending, category totals and budget breaches.")

if view.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

monthly = view.groupby("month", as_index=False)["amount"].sum()
category_totals = view.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
monthly_category = view.groupby(["month", "category"], as_index=False)["amount"].sum()
monthly_category["budget"] = monthly_category["category"].map(budgets).fillna(1000)
breaches = monthly_category[monthly_category["amount"] > monthly_category["budget"]].copy()
breaches["over_by"] = breaches["amount"] - breaches["budget"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total expenses", f"₹{view['amount'].sum():,.0f}")
c2.metric("Average monthly", f"₹{monthly['amount'].mean():,.0f}")
c3.metric("Highest category", category_totals.iloc[0]["category"])
c4.metric("Budget breaches", len(breaches))

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Monthly expense trend")
    trend = alt.Chart(monthly).mark_line(point=True).encode(
        x=alt.X("month:N", title="Month"),
        y=alt.Y("amount:Q", title="Expense (INR)", axis=alt.Axis(format="~s")),
        tooltip=[alt.Tooltip("month:N"), alt.Tooltip("amount:Q", format=",.0f")],
    ).properties(height=350)
    st.altair_chart(trend, use_container_width=True)

with right:
    st.subheader("Expense by category")
    category_chart = alt.Chart(category_totals).mark_bar(color="#4f46e5").encode(
        y=alt.Y("category:N", sort="-x", title="Category"),
        x=alt.X("amount:Q", title="Expense (INR)", axis=alt.Axis(format="~s")),
        tooltip=[alt.Tooltip("category:N"), alt.Tooltip("amount:Q", format=",.0f")],
    ).properties(height=350)
    st.altair_chart(category_chart, use_container_width=True)

st.subheader("Budget breach details")
if breaches.empty:
    st.success("No category exceeded its monthly budget in the selected view.")
else:
    st.dataframe(breaches.sort_values("over_by", ascending=False)[
        ["month", "category", "amount", "budget", "over_by"]
    ], use_container_width=True)

with st.expander("View cleaned transactions"):
    st.dataframe(view.sort_values("date", ascending=False)[
        ["transaction_id", "date", "category", "description", "amount", "payment_method"]
    ], use_container_width=True)
