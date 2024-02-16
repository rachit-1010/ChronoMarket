import pika 
from flask import Flask, request, g
from flask_cors import CORS
import json

app= Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})

# Context manager to handle RabbitMQ connection and channel lifecycle
class RabbitMQChannel:
    def __enter__(self):
        # Open a new connection and channel
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq-broker', port=5672))
        channel = connection.channel()
        channel.exchange_declare(exchange='timepiece-traders', exchange_type='topic')

        # Store the channel in the Flask context
        g.channel = channel

        return channel

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the channel and connection when the context manager is exited
        if 'channel' in g:
            g.channel.close()
            del g.channel


# define a single request endpoint to consume message requests from the frontend
# and publish messages to the message broker on the appropriate topic
@app.route('/api/message_broker', methods=['POST'])
def produce_new_message():
    """ Create a message for the RabbitMQ broker to consume based on a HTTP request from
     the frontend """  
    request_body = request.get_json()

    # load the routing key, and dump data dictionary into string
    message = json.dumps(request_body['data'])
    routing_key = request_body['topic']

    # create a unique channel for this connection
    # Use the RabbitMQChannel context manager to get a channel
    with RabbitMQChannel() as channel:
        channel.basic_publish(
            exchange='timepiece-traders', routing_key=routing_key, body=message)
    print(f" [x] Sent {routing_key}:{message}")
    return {}, 200

# # Close the RabbitMQ connection when the Flask application is shut down
# @app.teardown_appcontext
# def close_connection(exception=None):
#     if 'channel' in g:
#         g.channel.close()

# run message broker Flask service on port 3750
if __name__ == "__main__":
    app.run(port=3750, debug=True, host='0.0.0.0')