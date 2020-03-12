#!flask/bin/python
from flask import Flask, request, render_template
import requests
import razorpay
import json
from secrets import auth_key, DRF_SERVER_URL, HOST, PORT, RAZORPAY_APP_ID, RAZORPAY_APP_SECRET
razorpay_client = razorpay.Client(auth=(RAZORPAY_APP_ID, RAZORPAY_APP_SECRET))
app = Flask(__name__)


@app.route('/payment/success', methods=['POST'])
def payment_success():
    payment_success_data = request.form.to_dict()
    headers = {
        'authkey': auth_key
    }

    url = DRF_SERVER_URL + "/api/android/v1/payment/success"
    ret = requests.post(url, headers=headers, data=payment_success_data)
    status_code = ret.status_code
    # todo: handle if response is not 200 return something
    if status_code is 200:
        return render_template('payment_success.html')


@app.route('/payment/fail', methods=['POST'])
def payment_fail():
    headers = {
        'authkey': auth_key
    }
    data_in_bytes = request.data
    payment_fail_decoded_data = json.loads(data_in_bytes.decode("utf-8"))
    payment_fail_data = payment_fail_decoded_data['payload']['payment']['entity']
    print(payment_fail_data)
    url = DRF_SERVER_URL + "/api/android/v1/payment/fail"
    ret = requests.post(url, headers=headers, data=payment_fail_data)
    status_code = ret.status_code
    # todo: handle if response is not 200 return something
    if status_code is 200:
        return render_template('payment_fail.html')


@app.route('/payment/response', methods=['POST'])
def payment_response():
    headers = {
        'authkey': auth_key
    }
    data_in_bytes = request.data
    payment_fail_decoded_data = json.loads(data_in_bytes.decode("utf-8"))
    payment_fail_data = payment_fail_decoded_data['payload']['payment']['entity']
    print(payment_fail_data)
    url = DRF_SERVER_URL + "/api/android/v1/payment/fail"
    ret = requests.post(url, headers=headers, data=payment_fail_data)
    status_code = ret.status_code
    # todo: handle if response is not 200 return something
    if status_code is 200:
        return render_template('payment_fail.html')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
