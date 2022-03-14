import json

import requests
from decouple import config

from core.cash_consumer import ConsumerCashIn
from core.cash_consumer import ConsumerCashOut
from worker_celery.celery_app import app


@app.task(name='get_cash_in', bind=True)
def get_cash_in(_):
    consumer = ConsumerCashIn(queue="chash_in")
    consumer.run()


@app.task(name='get_cash_out', bind=True)
def get_cash_out(_):
    consumer = ConsumerCashOut(queue="chash_out")
    consumer.run()


@app.task(name='check', bind=True, time_limit=20)
def check(_):
    output = 'cache ok'
    return dict(output=output)
