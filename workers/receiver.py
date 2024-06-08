#!/usr/bin/env python  # Shebang line to indicate the script should be run with the Python interpreter
import pika  # Import the pika library to work with RabbitMQ
import time  # Import the time library to simulate work by sleeping

# Establish a connection to the RabbitMQ server running on the local machine
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()  # Create a channel through which to communicate with RabbitMQ

# Declare a queue named 'task_queue' and make it durable (persistent)
channel.queue_declare(queue='task_queue', durable=True)

# Print a message indicating the worker is waiting for messages
print(' [*] Waiting for messages. To exit press CTRL+C')

# Define the callback function that will be called when a message is received
def callback(ch, method, properties, body):
    # Print the received message
    print(" [x] Received %r" % body.decode())
    # Simulate work by sleeping for a number of seconds equal to the count of '.' characters in the message
    time.sleep(body.count(b'.'))
    # Print a message indicating the work is done
    print(" [x] Done")
    # Send an acknowledgment to RabbitMQ that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Configure the worker to only fetch one message at a time to avoid overwhelming it
channel.basic_qos(prefetch_count=1)
# Tell RabbitMQ that the callback function should receive messages from 'task_queue'
channel.basic_consume(queue='task_queue', on_message_callback=callback)

# Start consuming messages from the queue
channel.start_consuming()