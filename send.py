import sys
from .message_bus import MessageBus

try:
    service = sys.argv[1]
except IndexError:
    exit(' [*] No service')

try:
    message = sys.argv[2]
except IndexError:
    exit(' [*] No message')

bus = MessageBus()

correlation_id = bus.publish(service, message)

bus.receive(service, correlation_id)
fmt_string = " [*] Trying to correlate {0} for '{1}'"
print(fmt_string.format(correlation_id, service))

while bus.result is None:
    bus.connection.process_data_events()

print(" [x] We have a result: {0}".format(bus.result))
