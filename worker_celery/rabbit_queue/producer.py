import json

import pika

from worker_celery.config import get_config

config = get_config()


class Producer:
    def __init__(
        self,
        exchange="streaming",
        exchange_type="direct",
        heartbeat=0,
        broker_host=config.BROKER_HOST,
        broker_user=config.BROKER_USER,
        broker_pass=config.BROKER_PASS,
        broker_port=config.BROKER_PORT,
    ):
        self._exchange = exchange
        self._exchange_type = exchange_type
        self._parameters = pika.ConnectionParameters(
            host=broker_host,
            port=broker_port,
            credentials=pika.PlainCredentials(broker_user, broker_pass),
            heartbeat=heartbeat,
            virtual_host="dev",
        )
        self._properties = pika.BasicProperties(content_type="application/json", delivery_mode=2)
        self._connection = None
        self._channel = None
        self._connection = pika.BlockingConnection(self._parameters)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange, exchange_type=self._exchange_type)

    def publish(self, routing_key, message):
        """Method for publishing messages to the queue.

        Parameters
        ----------
        routing_key : str
            Queue route key.
        message : dict
            Object data to be sent.
        """
        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=self._properties,
        )

    def close(self):
        """Disconnect from RabbitMQ connection."""
        self._connection.close()
