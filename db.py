import sqlite3
import datetime

DB_NAME = 'finance.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incomes
                 (id INTEGER PRIMARY KEY, amount REAL, source TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY, amount REAL, category TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY, name TEXT, amount REAL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_income(amount, source):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO incomes (amount, source) VALUES (?, ?)", (amount, source))
    conn.commit()
    conn.close()

def add_expense(amount, category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))
    conn.commit()
    conn.close()

def add_payment(name, amount):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO payments (name, amount) VALUES (?, ?)", (name, amount))
    conn.commit()
    conn.close()

def get_incomes():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM incomes ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_payments():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM payments ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_balance():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM incomes")
    income_sum = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM expenses")
    expense_sum = c.fetchone()[0] or 0
    conn.close()
    return income_sum - expense_sum

def get_expenses_by_category():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = c.fetchall()
    conn.close()
    return {
        "labels": [r[0] for r in rows],
        "values": [r[1] for r in rows]
    }

def get_monthly_summary():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT strftime('%Y-%m', date), SUM(amount) FROM incomes GROUP BY strftime('%Y-%m', date)")
    incomes = dict(c.fetchall())
    c.execute("SELECT strftime('%Y-%m', date), SUM(amount) FROM expenses GROUP BY strftime('%Y-%m', date)")
    expenses = dict(c.fetchall())
    conn.close()
    months = sorted(set(incomes.keys()) | set(expenses.keys()))
    return {
        "labels": months,
        "incomes": [incomes.get(m, 0) for m in months],
        "expenses": [expenses.get(m, 0) for m in months]
    }

def get_forecast(months=6):
    balance = get_balance()
    now = datetime.date.today()
    labels, values = [], []
    for i in range(months):
        next_month = (now.month + i - 1) % 12 + 1
        year = now.year + (now.month + i - 1) // 12
        labels.append(f"{year}-{next_month:02d}")
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT SUM(amount) FROM payments")
        pay_sum = c.fetchone()[0] or 0
        conn.close()
        balance -= pay_sum
        values.append(balance)
    return {"labels": labels, "values": values}
