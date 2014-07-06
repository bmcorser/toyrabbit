import time
from .message_bus import MessageBus


def echo(body):
    print(" [x] Received: {0}".format(body))
    time.sleep(1)
    return body

bus = MessageBus()
route, queue, reply_route = bus.add_service_worker(echo)
fmt_string = " [*] service_route({0})"\
                      " --> worker_queue({1}) --> reply_route({2})"
print fmt_string.format(route, queue, reply_route)
bus.channel.start_consuming()
