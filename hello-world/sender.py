import pika  # Import the Pika library, which allows interaction with RabbitMQ

# Establish a connection to RabbitMQ server on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

# Create a communication channel
channel = connection.channel()

# Declare a queue named 'hello'. This creates the queue if it does not already exist.
channel.queue_declare(queue='hello')

# Publish a message to the 'hello' queue. 
# The empty string ('') as the exchange parameter specifies the default exchange.
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

# Print a confirmation message to the console
print(" [x] Sent 'Hello World!'")

# Close the connection to the RabbitMQ server
connection.close()
