import json
from uuid import uuid4
import pika
from pika import BasicProperties as Props
import logging

logging.basicConfig()


class MessageBus(object):

    exchange_params = {
        'exchange': 'central_direct',
        'type': 'direct',
    }
    result = None

    def __init__(self):
        connection_params = pika.ConnectionParameters('localhost')
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.exchange_declare(**self.exchange_params)

        self.connection = connection
        self.channel = channel

    @staticmethod
    def service_reply(service):
        return "{0}.reply".format(service)

    @staticmethod
    def func_reply(func):
        return "{0}.reply".format(func.__name__)

    def add_service_worker(self, func):
        service_queue = func.__name__
        self.channel.queue_declare(service_queue)

        reply = self.func_reply(func)
        self.channel.queue_declare(reply)
        reply_queue_bind = {
            'exchange': self.exchange_params['exchange'],
            'queue': reply,
            'routing_key': reply,
        }
        self.channel.queue_bind(**reply_queue_bind)

        def service(channel, method, properties, body):
            reply_properties = {
                'correlation_id': properties.correlation_id,
                'delivery_mode': 2,
            }
            publish_params = {
                'exchange': self.exchange_params['exchange'],
                'routing_key': reply,
                'properties': Props(**reply_properties),
                'body': json.dumps(func(body)),
            }
            channel.basic_publish(**publish_params)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        service_queue_bind = {
            'queue': service_queue,
            'exchange': self.exchange_params['exchange'],
            'routing_key': func.__name__,
        }
        self.channel.queue_bind(**service_queue_bind)
        self.channel.basic_consume(service, queue=service_queue)
        return func.__name__, service_queue, reply

    def receive(self, service, correlation_id):
        reply = self.service_reply(service)

        def correlate(channel, method, properties, body):
            if properties.correlation_id == correlation_id:
                self.result = body

        self.channel.basic_consume(correlate, queue=reply, no_ack=True)

    def publish(self, service, body):
        correlation_id = str(uuid4())
        reply = self.service_reply(service)

        properties = {
            'reply_to': reply,
            'content_type': 'application/json',
            'delivery_mode': 2,
            'correlation_id': correlation_id,
        }
        self.channel.basic_publish(exchange=self.exchange_params['exchange'],
                                   routing_key=service,
                                   properties=Props(**properties),
                                   body=body)
        return correlation_id
