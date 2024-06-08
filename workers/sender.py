#!/usr/bin/env python  # Shebang line to indicate the script should be run with the Python interpreter
import pika  # Import the pika library to work with RabbitMQ
import sys  # Import the sys library to access command-line arguments

# Establish a connection to the RabbitMQ server running on the local machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()  # Create a channel through which to communicate with RabbitMQ

# Declare a queue named 'task_queue' and make it durable (persistent)
channel.queue_declare(queue='task_queue', durable=True)

# Concatenate command-line arguments to form the message or use "Hello World!" if no arguments are provided
message = ' '.join(sys.argv[1:]) or "Hello World!"

# Publish the message to the 'task_queue' with persistence properties
channel.basic_publish(
    exchange='',  # Default exchange
    routing_key='task_queue',  # Queue to send the message to
    body=message,  # Message body
    properties=pika.BasicProperties(
        delivery_mode=2,  # Make message persistent
    ))

# Print a confirmation message to the console
print(" [x] Sent %r" % message)

# Close the connection to RabbitMQ
connection.close()
