from flask import Flask, render_template, request, redirect, url_for
import db
db.init_db()


app = Flask(__name__)

@app.route('/')
def index():
    balance = db.get_balance()
    return render_template('index.html', balance=balance)

@app.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        source = request.form['source']
        db.add_income(amount, source)
        return redirect(url_for('income'))
    incomes = db.get_incomes()
    return render_template('income.html', incomes=incomes)

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        db.add_expense(amount, category)
        return redirect(url_for('expenses'))
    expenses = db.get_expenses()
    return render_template('expenses.html', expenses=expenses)

@app.route('/payments', methods=['GET', 'POST'])
def payments():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        db.add_payment(name, amount)
        return redirect(url_for('payments'))
    payments = db.get_payments()
    return render_template('payments.html', payments=payments)

@app.route('/analytics')
def analytics():
    expenses_by_category = db.get_expenses_by_category()
    monthly_summary = db.get_monthly_summary()
    forecast = db.get_forecast(6)
    return render_template(
        'analytics.html',
        expenses_by_category=expenses_by_category,
        monthly_summary=monthly_summary,
        forecast=forecast
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
