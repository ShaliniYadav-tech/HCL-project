-- 1. Monthly totals and month-over-month change
SELECT substr(expense_date, 1, 7) AS month,
       ROUND(SUM(amount), 2) AS monthly_expense,
       ROUND(SUM(amount) - LAG(SUM(amount)) OVER (ORDER BY substr(expense_date, 1, 7)), 2) AS change_inr
FROM expenses
WHERE transaction_type = 'Expense'
GROUP BY substr(expense_date, 1, 7)
ORDER BY month;

-- 2. Category totals and share of spending
WITH category_totals AS (
    SELECT category, SUM(amount) AS total_amount
    FROM expenses
    WHERE transaction_type = 'Expense'
    GROUP BY category
)
SELECT category,
       ROUND(total_amount, 2) AS total_amount,
       ROUND(100.0 * total_amount / SUM(total_amount) OVER (), 2) AS spending_share_pct
FROM category_totals
ORDER BY total_amount DESC;

-- 3. Monthly budget breaches
SELECT substr(e.expense_date, 1, 7) AS month,
       e.category,
       ROUND(SUM(e.amount), 2) AS spent,
       b.monthly_budget,
       ROUND(SUM(e.amount) - b.monthly_budget, 2) AS over_budget
FROM expenses e
JOIN budgets b ON b.category = e.category
WHERE e.transaction_type = 'Expense'
GROUP BY substr(e.expense_date, 1, 7), e.category, b.monthly_budget
HAVING SUM(e.amount) > b.monthly_budget
ORDER BY over_budget DESC;
