toy-rabbit
==========

A tiny and very unstable message bus in Python that uses RabbitMQ.

There are two worker modules which run little services that sit and listen for
messages, process them and push the results out to their respective reply
queues, a `send` module to send messages to servies

### echoworker
```bash
python -m toyrabbit.echoworker
```
It just echoes whatever message you send.

### opworker
```bash
python -m toyrabbit.opworker
```
Will do simple mathemetical calculations. Expects JSON in the format:
```json
['<operator>', [<int>, <int>]]
```
Where the left side is one of `'*'` `'+'` `'/'` `'-'` and the right side is
a 2-tup of integer arguments.

### send
Send a message to one of the workers.
```bash
python -m toyrabbit.send <service> <message> [wait]
```
If `wait` is passed as the final argument, we will wait for the results; if it
isn't, an identifier will be returned that can be used with the `poll` module
to fetch the result later.

Examples:
```bash
$ python -m toyrabbit.send op '["*", [123, 456]]' wait
56088
```
```bash
$ python -m toyrabbit.send op '["/", [22, 7]]'
20f686fe-480f-4592-8efd-4380bd66c7c5
```

### poll
Poll for a result against a service with a correlation ID.
```bash
$ python -m toyrabbit.poll <service> <correlation> [wait]
```
If `wait` is passed, we will wait for the results; if it's not we will try once and return the correlation ID if the latest message on the reply queue for the service is not the one we want.

Example:
```bash
$ python -m toyrabbit.poll op 20f686fe-480f-4592-8efd-4380bd66c7c5 wait
3.142857142857143
```
