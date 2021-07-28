#!flask/bin/python
from flask import Flask, request, render_template
import requests
import razorpay
import json
from secrets import CLIENT_ID, CLIENT_SECRET, DRF_SERVER_URL, HOST, PORT, RAZORPAY_APP_ID, RAZORPAY_APP_SECRET, \
    FRONTEND_HOST, ELASTIC_SEARCH_HOST
from es_logger import PaymentLogs

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=ELASTIC_SEARCH_HOST)

razorpay_client = razorpay.Client(auth=(RAZORPAY_APP_ID, RAZORPAY_APP_SECRET))
app = Flask(__name__, template_folder='templates')

drf_endpoint_headers = {
    'Authorisation': CLIENT_ID + "-" + CLIENT_SECRET,
}

RAZOR_ORDER_ID = 'razor_order_id'
RAZOR_PAYMENT_ID = 'razor_payment_id'
RAZOR_SIGNATURE = 'razor_signature'


@app.route('/payment/success', methods=['POST'])
def payment_success():
    try:
        body = 'initiating payment success from web'
        keyword = 'payment-success-from-web'

        payment_success_data = request.form.to_dict()
        '''
        payment success data body will send back a dict with
        { 
            'order_id': 'order_abc123', 
            'razorpay_payment_id': 'pay_xyz123', 
            'razorpay_order_id': 'razorpay_order_id', 
            'razorpay_signature': 'a-really-long-string' 
        } 
        '''

        url = DRF_SERVER_URL + "/api/android/v1/payment/verify"
        ret = requests.post(url, headers=drf_endpoint_headers, data={
            RAZOR_ORDER_ID: payment_success_data['razorpay_order_id'],
            RAZOR_PAYMENT_ID: payment_success_data['razorpay_payment_id'],
            RAZOR_SIGNATURE: payment_success_data['razorpay_signature'],
        })
        status_code = ret.status_code
        # todo: handle if response is not 200 return something
        host = "http://%s:%s/" % (request.remote_addr, str(request.environ['REMOTE_PORT']))
        if status_code is 200:
            # body += '-successfully done payment from web with status 200 from drf'
            # payment_log = PaymentLogs()
            # payment_log.save_payment_log_in_elasticsearch(body=body, keyword=keyword) 
            # payment_log.save()
            return render_template('payment_success.html', host=FRONTEND_HOST)
        else:
            # body += '-failed payment from web with status ' + str(status_code) + ' from drf'
            # payment_log = PaymentLogs()
            # payment_log.save_payment_log_in_elasticsearch(body=body, keyword=keyword)
            # payment_log.save()
            return render_template('payment_fail.html', host=FRONTEND_HOST), 500
    except Exception as e:
        print(e)
        # body = 'initiating payment success from web c' \
        #        'ounter error-' + str(e)
        # keyword = 'payment-success-from-web'
        # payment_log = PaymentLogs()
        # payment_log.save_payment_log_in_elasticsearch(body=body, keyword=keyword)
        # payment_log.save()
        return render_template('payment_fail.html', host=FRONTEND_HOST), 500


@app.route('/payment/fail', methods=['POST'])
def payment_fail():
    try:
        body = 'initiating payment fail from microservice'
        keyword = 'payment-fail-from-micoservice'
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
        # host = "http://%s:%s/" % (request.remote_addr, str(request.environ['REMOTE_PORT']))
        if status_code is 200:
            # body += '-done fail payment with status 200 from drf'
            # payment_log = PaymentLogs()
            # payment_log.save_payment_log_in_elasticsearch(body=body, keyword=keyword)
            # payment_log.save()
            return render_template('payment_fail.html', host=FRONTEND_HOST), 200
        else:
            # body += '-failed to fail payment' + ' with status ' + str(status_code) + ' from drf'
            # payment_log = PaymentLogs()
            # payment_log.save_payment_log_in_elasticsearch(body=body, keyword=keyword)
            # payment_log.save()
            return render_template('payment_fail.html', host=FRONTEND_HOST), 500
    except Exception as e:
        print(e)
        # body = '-payment fail from microservice failed with error-' + str(e)
        # keyword = 'payment-fail-from-micoservice'
        # payment_log = PaymentLogs()
        # payment_log.save_payment_log_in_elasticsearch(body=body, keyword=keyword)
        # payment_log.save()
        return render_template('payment_fail.html', host=FRONTEND_HOST), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
