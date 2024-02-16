import pika
import requests
import json
import time
import socket
from datetime import datetime


# loop until container is ready to allow RabbitMQ connection
while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq-broker', port=5672))
        channel = connection.channel()
        break
    except pika.exceptions.AMQPConnectionError:
        print("Waiting for RabbitMQ to be ready...")
        time.sleep(5)

# declare the exchange to listen in on
channel.exchange_declare(exchange='timepiece-traders', exchange_type='topic')

# declare a random queue for messages consumed by this service to be added to
# and eventually executed
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange with the items specific routing pattern
routing_pattern = "*.items.*"
channel.queue_bind(exchange='timepiece-traders',
                   queue=queue_name, routing_key=routing_pattern)

# define a function to be called when this consumer finds a message matching its routing pattern


def callback(ch, method, properties, body):
    # try decoding the message
    try:
        message = json.loads(body)
        routing_key = method.routing_key
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return

    # the notification type is the last portion of the routing_key pattern
    notification_type = routing_key.split(".")[2]
    print("notification type: " + notification_type)
    print(message)

    ######################### NEED TO DO ################################################
    # 1. Depending on the notification_type, send to appropriate Flask Notification endpoint
    # - can map notification_type values 1:1 with /XXX endpoint in notifications.py
    # 2. Parse out the "message" as needed to send body/input to Flask endpoints for email,
    # such as the username

    # the topics that I'm listening to
    if notification_type == "purchased":
        print(f'message received: {message}')
        user_id = message['user_id']
        item_id = message['item_id']
        purchase_amount = message['purchase_amount']
        status = "in-cart"  # items won through bidding are sent to the cart
        # Format this as your API expects
        purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Prepare data for the API request
        purchase_data = {
            "user_id": user_id,
            "item_id": item_id,
            "status": status,
            "purchase_date": purchase_date,
            "purchase_amount": purchase_amount
        }

        # Make the API request
        host_ip = socket.gethostbyname('host.docker.internal')
        headers = {
            "Content-Type": "application/json"}
        response = requests.post(
            f"http://{host_ip}:3500/api/item/add_purchase", json=purchase_data, headers=headers)
        print(response.text)


# Set up the consumer with a callback function for when it receives a message
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()
