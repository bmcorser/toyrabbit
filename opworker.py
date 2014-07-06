import json
import operator
from .message_bus import MessageBus

O = {
    '*': operator.mul,
    '+': operator.add,
    '/': operator.div,
    '-': operator.sub,
}


def op(body):
    print(" [x] Received: {0}".format(body))
    sym, args = json.loads(body)
    return O[sym](*args)

bus = MessageBus()
route, queue, reply_route = bus.add_service_worker(op)
fmt_string = " [*] service_route({0})"\
                        " --> worker_queue({1}) --> reply_route({2})"
print fmt_string.format(route, queue, reply_route)
bus.channel.start_consuming()
