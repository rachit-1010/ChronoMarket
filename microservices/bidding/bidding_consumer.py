import pika
import requests
import json
import time
import socket
from datetime import datetime


host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

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
routing_pattern = "*.bidding.*"
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
    print(f'receiving from auction_auto_change: {message}')

    # the topics that I'm listening to
    if notification_type == "emails":
        docker_host_ip = socket.gethostbyname('host.docker.internal')

        notifications = message['notifications']
        seller_email = message['seller_email']
        seller_id = message['seller_id']
        item_id = message['item_id']
        item_name = message['item_name']

        # Make the fetch request to my bidding endpoint
        headers = {"Content-Type": "application/json"}

        emails = []
        # Update with the correct host and port
        url = f'http://{docker_host_ip}:9900/api/bidding/bidders/{item_id}'
        try:
            response = requests.get(url)

            if response.status_code == 200:
                bidders_data = response.json()
                emails = [json.loads(bidder)[1]
                          for bidder in bidders_data]  # Extracting emails
                print(emails)  # List of emails

            else:
                print('Failed to retrieve bidders:', response.status_code)

        except requests.exceptions.RequestException as e:
            print('Error making request:', e)

        emails.append(seller_email)

        # Setup the data to send to RabbitMQ
        data = {'data': {'email': emails, 'auction': item_name},
                'topic': f'request.notifications.{notifications}'}

        # Send the data to RabbitMQ
        response = requests.post(
            f'http://rabbitmq-flask-server:3750/api/message_broker', json=data, headers=headers)

        if response.status_code == 200:
            print(
                f" [x] Sent request.notifications.{notifications}")
        else:
            print(
                f" [!] Failed to send message for auction")

        if notifications == 'auction_end':

            # GET HIGHEST BID INFORMATION FROM BIDDING
            url = f'http://{docker_host_ip}:9900/api/bidding/highestbid/{item_id}'
            try:
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    bidding_data = response.json()

                    highest_bid = bidding_data.get('bid_amount')
                    user_id = bidding_data.get('user_id')
                    user_email = bidding_data.get('user_email')
                    print(f"bidder's id: {user_id}")
                    print(f'highest bid: {highest_bid}')
                    print(f"bidder's email: {user_email}")

                
                    # Setup the data to send to RabbitMQ for WINNING BID
                    data = {'data': {'email': user_email, 'auction': item_name},
                            'topic': f'request.notifications.winning_bid'}

                    # Send the data to RabbitMQ
                    response = requests.post(
                        f'http://rabbitmq-flask-server:3750/api/message_broker', json=data, headers=headers)

                    if response.status_code == 200:
                        print(
                            f" [x] Sent request.notifications.{notifications}")
                    else:
                        print(
                            f" [!] Failed to send message for auction")

                else:
                    print('Failed to retrieve highest bid:',
                          response.status_code)

            except requests.exceptions.RequestException as e:
                print('Error making request:', e)

            if highest_bid == 'No bids yet':
                highest_bid = 0
                user_id = 0


            # SEND PURCHASE PRICE TO SEND TO REDIS
            url = f'http://{docker_host_ip}:9900/api/bidding/purchase_price/{item_id}'

            data = {
                'purchase_price': highest_bid
            }

            try:
                response = requests.post(url, json=data, headers=headers)

                if response.status_code == 200:
                    print("Purchase added successfully to Redis")
                else:
                    print('Failed to add to redis', response.status_code)

            except requests.exceptions.RequestException as e:
                print('Error making request:', e)

            # Setup the data to send to RabbitMQ
            data = {'data': {'user_id': user_id,
                             'item_id': item_id,
                             'purchase_amount': highest_bid},
                    'topic': 'request.items.purchased'}

            # Send the data to RabbitMQ
            response = requests.post(
                f'http://rabbitmq-flask-server:3750/api/message_broker', json=data, headers=headers)

            if response.status_code == 200:
                print(
                    f" [x] Sent request.notifications.{notifications}")
            else:
                print(
                    f" [!] Failed to send message for auction")


# Set up the consumer with a callback function for when it receives a message
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
channel.start_consuming()
