import pika
import requests
import json
import time
import socket

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

# Bind the queue to the exchange with the notifications specific routing pattern
routing_pattern = "*.notifications.*"
channel.queue_bind(exchange='timepiece-traders', queue=queue_name, routing_key=routing_pattern)




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
    if notification_type == "auction_end":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # auction name
        post_to_endpoints("auction_end", message)


    elif notification_type == "one_hour":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # auction name
        post_to_endpoints("one_hour", message)


    elif notification_type == "one_day":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # auction name
        post_to_endpoints("one_day", message)


    elif notification_type == "winning_bid":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # auction name
        post_to_endpoints("winning_bid", message)


    elif notification_type == "watchlist":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # item name (or the auction name, doesnt matter, just lmk)
        post_to_endpoints("watchlist", message)
    

    elif notification_type == "high_bid":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # auction name
        post_to_endpoints("high_bid", message)


    elif notification_type == "respond_feedback":
        # needed info:
            # recipient emails (either list of many/one emails or string of one email)
            # subject of the email to send
            # body info of the email to send

        post_to_endpoints("respond_feedback", message)

    elif notification_type == "update_feedback":
        # needed info:
            # feedback id

        post_to_endpoints("update_feedback", message)


    elif notification_type == "seller_new_bid":

        post_to_endpoints("seller_new_bid", message)
            




    # # make API request and print the response
    # host_ip = socket.gethostbyname('host.docker.internal')
    # response = requests.get(f"http://{host_ip}:3900/api/accounts/admin/list",)
    # print(response.text)

# posting to endpoints
def post_to_endpoints(endpoint, message):
    host_ip = socket.gethostbyname('host.docker.internal')

    headers = {
        "Content-Type": "application/json"
    }

    url = f"http://{host_ip}:7777/api/notifications/{endpoint}"
    # response = requests.post(url, json={"message": message})
    response = requests.post(url, json=message, headers=headers)
    print(response.text)



# Set up the consumer with a callback function for when it receives a message
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()