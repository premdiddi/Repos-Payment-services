import unittest

from app import app
from app import RAZOR_ORDER_ID, RAZOR_PAYMENT_ID, RAZOR_SIGNATURE


class PaymentSuccessTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_url_function_mapping(self):
        url_matched = False
        url_function_mapper = self.app.application.url_map._rules
        for single_function in url_function_mapper:
            if '/payment/success' == single_function.rule:
                url_matched = True
                self.assertEqual(single_function.endpoint, 'payment_success')
        if not url_matched:
            # throw error
            self.assertEqual(1, 0)

    def test_payment_success_input(self):
        # Given

        # Then
        self.assertEqual(RAZOR_ORDER_ID, 'razor_order_id')
        self.assertEqual(RAZOR_PAYMENT_ID, 'razor_payment_id')
        self.assertEqual(RAZOR_SIGNATURE, 'razor_signature')

    def tearDown(self):
        pass
        # Delete Database collections after the test is complete


class PaymentFailTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_url_function_mapping(self):
        url_matched = False
        url_function_mapper = self.app.application.url_map._rules
        for single_function in url_function_mapper:
            if '/payment/fail' == single_function.rule:
                url_matched = True
                self.assertEqual(single_function.endpoint, 'payment_fail')
        if not url_matched:
            # throw error
            self.assertEqual(1, 0)

    def tearDown(self):
        pass
        # Delete Database collections after the test is complete
