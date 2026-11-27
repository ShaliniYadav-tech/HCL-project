CREATE TABLE IF NOT EXISTS expenses (
    transaction_id TEXT PRIMARY KEY,
    expense_date DATE NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL,
    transaction_type TEXT NOT NULL,
    payment_method TEXT
);

CREATE TABLE IF NOT EXISTS budgets (
    category TEXT PRIMARY KEY,
    monthly_budget REAL NOT NULL
);
