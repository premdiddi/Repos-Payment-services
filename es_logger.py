from elasticsearch_dsl import Document, Date, Keyword, Text, Integer, Float
from secrets import ES_PAYMENT_LOGS_INDEX


class PaymentLogs(Document):
    platform = Text()
    env = Text()
    title = Text()
    user_id = Integer()
    mobile = Text()
    customer_id = Integer()
    user_name = Text()
    order_id = Text()
    customer_name = Text()
    quantity = Float()
    amount = Float()
    body = Text()
    status = Text()
    keyword = Text()
    payment_method = Text()
    tags = Keyword()
    timestamp = Date()
    pg_response_body = Text()

    class Index:
        name = ES_PAYMENT_LOGS_INDEX
        # settings = {
        #   "number_of_shards": 2,
        # }

    def save_payment_log_in_elasticsearch(self, platform=None, title=None, user_id=None, order_id=None, mobile=None, customer_id=None,
                                          user_name=None, customer_name=None, quantity=None, amount=None, body=None,
                                          status=None, keyword=None, payment_method=None, tags=None, timestamp=None,
                                          pg_response_body=None, env=None):
        self.platform = platform
        self.title = title
        self.user_id = user_id
        self.mobile = mobile
        self.customer_id = customer_id
        self.order_id = order_id
        self.user_name = user_name
        self.customer_name = customer_name
        self.quantity = quantity
        self.amount = amount
        self.body = body
        self.status = status
        self.keyword = keyword
        self.payment_method = payment_method
        self.tags = tags
        self.timestamp = timestamp
        self.pg_response_body = pg_response_body
        self.env = env

        self.save()
