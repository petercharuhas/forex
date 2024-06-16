from flask import Flask, request, render_template, jsonify
from forex_python.converter import CurrencyRates, CurrencyCodes


app = Flask(__name__)
currency_rates = CurrencyRates()
currency_codes = CurrencyCodes() 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    currency_from = request.form['currency_from']
    currency_to = request.form['currency_to']
    amount = request.form['amount']
    
    # Validate inputs
    error_message = None
    try:
        amount = float(amount)
    except ValueError:
        error_message = "Invalid amount. Please enter a number."
    
    if not currency_rates.get_rate(currency_from, 'USD'):
        error_message = f"Invalid 'from' currency: {currency_from}."
    
    if not currency_rates.get_rate(currency_to, 'USD'):
        error_message = f"Invalid 'to' currency: {currency_to}."
    
    if error_message:
        return render_template('index.html', error=error_message)

    # Perform conversion
    converted_amount = currency_rates.convert(currency_from, currency_to, amount)
    currency_symbol = currency_codes.get_symbol(currency_to)
    result = f"{currency_symbol} {converted_amount:.2f}"
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(port=5001)

