#!flask/bin/python
from flask import Flask, request, render_template
import requests
import razorpay
import json
from secrets import CLIENT_ID, CLIENT_SECRET, DRF_SERVER_URL, HOST, PORT, RAZORPAY_APP_ID, RAZORPAY_APP_SECRET

razorpay_client = razorpay.Client(auth=(RAZORPAY_APP_ID, RAZORPAY_APP_SECRET))
app = Flask(__name__, template_folder='templates')

drf_endpoint_headers = {
    'Authorisation': CLIENT_ID + "-" + CLIENT_SECRET,
}


@app.route('/payment/success', methods=['POST'])
def payment_success():
    payment_success_data = request.form.to_dict()
    '''
    payment success data body will send back a dict with
    { 
        'order_id': 'order_abc123', 
        'razorpay_payment_id': 'pay_xyz123', 
        'razorpay_order_id': 'order_abc123', 
        'razorpay_signature': 'a-really-long-string' 
    } 
    '''

    url = DRF_SERVER_URL + "/api/android/v1/payment/verify"
    ret = requests.post(url, headers=drf_endpoint_headers, data={
        'razor_order_id': payment_success_data['razorpay_order_id'],
        'razor_payment_id': payment_success_data['razorpay_payment_id'],
        'razor_signature': payment_success_data['razorpay_signature'],
    })
    status_code = ret.status_code
    # todo: handle if response is not 200 return something
    # todo: logging
    host = "http://%s:%s/" % (request.remote_addr, str(request.environ['REMOTE_PORT']))
    if status_code is 200:
        return render_template('payment_success.html', host=host)
    else:
        # todo: logging
        return render_template('payment_fail.html', host=host), 500


@app.route('/payment/fail', methods=['POST'])
def payment_fail():
    # todo: validate auth key of webhook
    data_in_bytes = request.data
    payment_fail_decoded_data = json.loads(data_in_bytes.decode("utf-8"))
    payment_fail_data = payment_fail_decoded_data['payload']['payment']['entity']
    print(payment_fail_data)
    url = DRF_SERVER_URL + "/api/android/v1/payment/fail"
    ret = requests.post(url, headers=drf_endpoint_headers, data=payment_fail_data)
    status_code = ret.status_code
    # todo: handle if response is not 200 return something
    # todo: logging
    host = "http://%s:%s/" % (request.remote_addr, str(request.environ['REMOTE_PORT']))
    if status_code is 200:
        return render_template('payment_fail.html', host=host), 500
    else:
        return render_template('payment_fail.html', host=host), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
