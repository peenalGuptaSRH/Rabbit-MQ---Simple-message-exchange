#!/usr/bin/env python
import pika, sys, os  # Import necessary libraries: Pika for RabbitMQ, sys and os for system operations

# Define the main function
def main():
    # Establish a connection to RabbitMQ server on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    
    # Create a communication channel
    channel = connection.channel()
    
    # Declare a queue named 'hello'. This creates the queue if it does not already exist.
    channel.queue_declare(queue='hello')
    
    # Define a callback function to handle messages received from the 'hello' queue
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
    
    # Set up subscription on the 'hello' queue. Whenever a message is received, the callback function is called.
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    
    # Print a message to indicate waiting for messages and instructions to exit
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    # Start consuming messages from the queue
    channel.start_consuming()

# Check if the script is run directly (not imported as a module)
if __name__ == '__main__':
    try:
        main()  # Call the main function
    except KeyboardInterrupt:
        print('Interrupted')  # Print message if interrupted with CTRL+C
        try:
            sys.exit(0)  # Attempt to exit gracefully
        except SystemExit:
            os._exit(0)  # Force exit if the graceful exit fails
