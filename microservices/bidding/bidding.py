from flask import Flask, request, jsonify
import redis
import json
from datetime import datetime
from flask_cors import CORS

"""
REDIS DATABASES

#Track current highest bid
    redis_client.hmset(f"item:{item_id}", bid_data)

# Track user's bid history
    redis_client.lpush(f"user:{user_id}:bids", json.dumps({'item_id': item_id, 'bid_amount': bid_amount, 'timestamp': datetime.now().isoformat()}))

# Track all bidders on an item
    redis_client.lpush(f"item:{item_id}:bidders", (user_id, user_email))

# Track previous highest bidder
    redis_client.hmset(f"item:{item_id}:previoushigh", current_bid)    

"""


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


@app.route('/api/bidding/bid', methods=['POST'])
def place_bid():
    """
    Place a bid on an item.
    Expects a JSON with 'user_id', 'username', 'item_id', 'user_email', and 'bid_amount'.
    """

    data = request.json

    user_id = data.get('user_id')
    username = data.get('username')
    item_id = data.get('item_id')
    user_email = data.get('user_email')
    bid_amount = data.get('amount')

    if not all([user_id, item_id, user_email, bid_amount]):
        return jsonify({"error": "Missing data"}), 400

    # Check and update the current highest bid
    current_bid = redis_client.hgetall(f"item:{item_id}")
    

    #Make sure the bid is higher than the current highest bid
    if current_bid.get('bid_amount') is not None:
        if int(current_bid.get('bid_amount')) >= int(bid_amount):
            return jsonify({"error": "Bid amount is too low"}), 400
        

    #Make sure the item hasn't been purchased yet
    # Check if the item_id already exists in Redis
    key = f"item:{item_id}:purchase_price"
    if redis_client.exists(key):
        return jsonify({"error": "Item has already been purchased"}), 400


    # Update highest bid
    bid_data = {
        'user_id': user_id,
        'username': username,
        'user_email': user_email,
        'bid_amount': bid_amount,
        'timestamp': datetime.now().isoformat()
    }

    # If there was a current bid, update the previous high and send a notification out
    if current_bid:
        redis_client.hmset(f"item:{item_id}:previoushigh", current_bid)
        

    redis_client.hmset(f"item:{item_id}", bid_data)

    # Track user's bid history
    redis_client.lpush(f"user:{user_id}:bids", json.dumps({'item_id': item_id, 'bid_amount': bid_amount, 'timestamp': datetime.now().isoformat()}))

    # Add user_id / email to the list of bidders for the item
    redis_client.lpush(f"item:{item_id}:bidders", json.dumps((user_id, user_email)))


    return jsonify({"message": "Bid placed successfully"}), 200




@app.route('/api/bidding/highestbid/<item_id>', methods=['GET'])
def get_bid(item_id):
    """
    Get the current highest bid for an item, which gives 
    - user_id
    - username
    - user_email
    - bid_amount
    - timestamp
    """
    
    bid_data = redis_client.hgetall(f"item:{item_id}")
    
    #Send empty data if there are no bids yet
    if not bid_data:        
        no_data = {
            'user_id': 'No bids yet',
            'username': 'No bids yet',
            'bid_amount': 'No bids yet',
            'user_email': 'No bids yet'
        }
        return jsonify(no_data), 200

    return jsonify(bid_data), 200



@app.route('/api/bidding/bidders/<item_id>', methods=['GET'])
def get_bidders(item_id):
    """
    Get the list of all bidders on an item

    Used for Auction Notifications - enables API to track everyone who has ever bid on a certain item ID
    and will be notified when the auction is nearing completion
    """
    
    bidders = redis_client.lrange(f"item:{item_id}:bidders", 0, -1)
    
    if not bidders:
        return jsonify({"error": "No bidders found for this item"}), 404

    return jsonify(bidders), 200



@app.route('/api/bidding/previoushigh/<item_id>', methods=['GET'])
def get_previous_highest_bidder(item_id):
    # Retrieve the highest bid (largest score) before the current highest
    # We use zrevrange to get items in descending order of their scores
    
    highest_bid = redis_client.hgetall(f"item:{item_id}:previoushigh")

    if not highest_bid:
        return None
    
    return highest_bid



@app.route('/api/bidding/<user_id>', methods=['GET'])
def get_user_bids(user_id):
    """
    Get all bids placed by a user.
    """
    
    bids = redis_client.lrange(f"user:{user_id}:bids", 0, -1)
    bids = [json.loads(bid) for bid in bids]

    return jsonify(bids), 200


@app.route('/api/bidding/purchase_price/<item_id>', methods=['GET', 'POST'])
def purchase_price(item_id):
    if request.method == 'POST':
        # Handle the POST request
        data = request.json
        purchase_price = data.get('purchase_price')

        if not purchase_price:
            return jsonify({"error": "Missing purchase price"}), 400

        # Store the purchase price in Redis
        redis_client.set(f"item:{item_id}:purchase_price", purchase_price)
        return jsonify({"message": "Purchase price stored successfully"}), 200


    elif request.method == 'GET':
        # Handle the GET request
        purchase_price = redis_client.get(f"item:{item_id}:purchase_price")

        if purchase_price is None:
            return jsonify({"error": "Purchase price not found"}), 404

        return jsonify({"purchase_price": purchase_price}), 200



if __name__ == '__main__':
    app.run(port=9900, debug=True, host='0.0.0.0')



