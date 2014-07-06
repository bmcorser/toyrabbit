import sys
from .message_bus import MessageBus

try:
    service = sys.argv[1]
except IndexError:
    exit('No service')

try:
    message = sys.argv[2]
except IndexError:
    exit('No message')

bus = MessageBus()

correlation_id = bus.publish(service, message)

try:
    if sys.argv[3] == 'wait':
        bus.receive(service, correlation_id)
        while bus.result is None:
            bus.connection.process_data_events()
        print(bus.result)
except IndexError:
    print(correlation_id)
