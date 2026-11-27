# Personal Expense Tracker and Budget Dashboard

Project 9 from the II Year Data Analyst Project List.

## Deliverables

- Reproducible sample expense dataset
- Cleaning and quarantine for duplicate, missing, negative and transfer records
- Monthly and category KPIs
- Budget breach report
- Matplotlib charts
- Interactive Streamlit dashboard
- SQLite-compatible SQL queries
- Power BI DAX measures

## Run

```bash
cd Personal_Expense_Tracker_Budget_Dashboard
python generate_expenses.py
python clean_expenses.py
python analysis_kpis_charts.py
streamlit run app/streamlit_app.py
```

Install the required Python packages with:

```bash
pip install pandas matplotlib streamlit altair
```
