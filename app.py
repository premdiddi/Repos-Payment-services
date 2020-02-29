#!flask/bin/python
from flask import Flask, request, render_template
import requests
from secrets import auth_key, DRF_SERVER_URL
app = Flask(__name__)


@app.route('/api/payment/success/', methods=['POST'])
def payment_success():
    payment_success_data = request.form.to_dict()
    headers = {
        'authkey': auth_key
    }

    url = DRF_SERVER_URL + "/api/android/v1/payment/success"
    ret = requests.post(url, headers=headers, data=payment_success_data)
    status_code = ret.status_code
    if status_code is 200:
        return render_template('payment_success.html')


@app.route('/api/payment/fail/', methods=['POST'])
def payment_fail():
    payment_fail_data = request.form.to_dict()
    headers = {
        'authkey': auth_key
    }

    url = DRF_SERVER_URL + "/api/android/v1/payment/fail"
    ret = requests.post(url, headers=headers, data=payment_fail_data)
    status_code = ret.status_code
    if status_code is 200:
        return render_template('payment_fail.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)