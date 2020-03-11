#!flask/bin/python
from flask import Flask, request, render_template
import requests
import razorpay
import json
from secrets import auth_key, DRF_SERVER_URL, HOST, PORT, RAZORPAY_APP_ID, RAZORPAY_APP_SECRET
razorpay_client = razorpay.Client(auth=(RAZORPAY_APP_ID, RAZORPAY_APP_SECRET))
app = Flask(__name__)


@app.route('/')
def app_create():
    return render_template('app.html')


@app.route('/generate_order_id', methods=['POST'])
def razorpay_generate_order():
    order_amount = 50000
    order_currency = 'INR'
    order_receipt = 'PRO-009093'
    # notes = {'Delivering address': 'Aundh, Pune'}  # OPTIONAL
    res = razorpay_client.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt,
                                       payment_capture='1')
    order_id = res['id']
    print('Razorpay order create api response', res)
    return json.dumps(res)


@app.route('/charge', methods=['POST'])
def app_charge():
    amount = 5100
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    return json.dumps(razorpay_client.payment.fetch(payment_id))


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)

# razorpay order create response
# {"id": "order_EQ8mP6AZQqNzZg", "entity": "order", "amount": 50000, "amount_paid": 0, "amount_due": 50000, "currency":
# "INR", "receipt": "PRO-009093", "offer_id": null, "status": "created", "attempts": 0, "notes": [], "created_at":
# 1583761376}
