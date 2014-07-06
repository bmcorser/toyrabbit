import sys
from .message_bus import MessageBus

bus = MessageBus()

try:
    service = sys.argv[1]
except IndexError:
    exit('No service')

try:
    correlation_id = sys.argv[2]
except IndexError:
    exit('No correlation ID')

bus.receive(service, correlation_id)
try:
    if sys.argv[3] == 'wait':
        while bus.result is None:
            bus.connection.process_data_events()
        print(bus.result)
except IndexError:
    bus.connection.process_data_events()
    if bus.result is None:
        print(correlation_id)
    else:
        print(bus.result)
