from functools import partial

import pika

from worker_celery.config import get_config
from worker_celery.rabbit_queue.exception import BrokerConnectionError

config = get_config()


class Consumer:
    def __init__(
            self,
            queue=config.QUEUE,
            rounting_key=config.ROUTING_KEY,
            exchange="streaming",
            exchange_type="direct",
            heartbeat=60,
            broker_host=config.BROKER_HOST,
            broker_user=config.BROKER_USER,
            broker_port=config.BROKER_PORT,
            broker_pass=config.BROKER_PASS,
    ):
        self._queue = queue
        self._routing_key = rounting_key
        parameters = pika.ConnectionParameters(
            host=broker_host,
            port=broker_port,
            credentials=pika.PlainCredentials(broker_user, broker_pass),
            heartbeat=heartbeat,
            virtual_host="dev",
        )

        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            raise BrokerConnectionError()

        self._channel = connection.channel()
        self._channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        self._channel.queue_declare(queue=queue, durable=True)
        self._channel.queue_bind(queue=queue, exchange=exchange, routing_key=self._routing_key)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=partial(self._callback),
            auto_ack=False,
        )

    def _callback(self, channel, method, properties, body):
        """Method for processing messages received by the message queue.

        Parameters
        ----------
        ch : pika.channel.Channel
            The channel object.
        method : pika.frame.Method
            Informed method.
        properties : pika.Spec.BasicProperties
            Infomed properties.
        body : str|unicode
            The message body.
        cb : function
            Callback function
        """
        self.callback_function(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        """Method to start queue consumption."""
        self._channel.start_consuming()

    def callback_function(self, body):
        print(body)

