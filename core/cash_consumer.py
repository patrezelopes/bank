import json

import jwt
import requests
from decouple import config

from worker_celery.rabbit_queue.consumer import Consumer
from worker_celery.rabbit_queue.producer import Producer


def pending_transaction(body, way):
    payload = json.loads(body.decode("utf-8"))
    headers = payload.get("headers", "")
    if headers:
        body = dict(**payload.get("body", ""), way=way)
        result = requests.post(url=f"http://{config('TRANSACTION_HOST')}/transaction/", json=body, headers=headers)
        return result
    else:
        return "nothing"


class ConsumerCashIn(Consumer):

    def callback_function(self, body):
        super().callback_function(self)
        result = pending_transaction(body=body, way='in')
        print(result)


class ConsumerCashOut(Consumer):

    def callback_function(self, body):
        super().callback_function(self)
        result = pending_transaction(body=body, way='out')
        print(result)
