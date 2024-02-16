from flask import request
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
import mysql.connector
import base64
import os
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})
BASE_DIR = os.path.dirname(__file__)
print("BASE DIRECTORY IS", BASE_DIR)


class APIResponse:
    """ Define a class for structuring API responses"""

    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_flask_response(self):
        return jsonify(self.data), self.status


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=6001,  # the port exposed in Docker
        user="user",
        password="password",
        database="mysql"
    )


@app.route('/api/item/add_item', methods=['POST'])
def add_item():
    # Extract fields from form data
    required_fields = ['user_id', 'item_name', 'description', 'watch_reference_number',
                       'watch_model', 'watch_year', 'brand', 'item_condition', 'auction_won',
                       'starting_price', 'bid_amount', 'auction_start', 'auction_deadline']
    missing_fields = [
        field for field in required_fields if not request.form.get(field)]
    print(missing_fields)
    print(request.form.get('brand'))
    if missing_fields:
        return APIResponse(f"Missing parameters: {', '.join(missing_fields)}", 400).to_flask_response()

    # Extract and format fields
    values = [request.form.get(field) for field in required_fields]

    # Handle the image file
    image = request.files.get('item_image')
    if image:
        # image_dir = os.path.join(
        #     BASE_DIR, 'watch-images')
        # image_path = os.path.join(image_dir, image.filename)
        # print(image_path)
        # image.save(image_path)
        # # Assuming you want to store the image path in the database
        # values.append(image_path)
        image_blob = image.read()
        values.append(image_blob)
    else:
        return APIResponse("Missing item image", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = """
    INSERT INTO items (user_id, item_name, description, watch_reference_number, 
                       watch_model, watch_year, brand, item_condition, auction_won, 
                       starting_price, bid_amount, auction_start, auction_deadline, item_image)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_query, tuple(values))
    db_connection.commit()
    item_id = cursor.lastrowid
    cursor.close()
    db_connection.close()
    return APIResponse({"item_id": item_id}, 200).to_flask_response()


@app.route('/api/item/update_item', methods=['POST'])
def update_item():
    """ Update an item """
    data = request.get_json()
    item_id = data.get('item_id')
    if not item_id:
        return APIResponse("Missing item_id", 400).to_flask_response()

    update_fields = []
    values = []
    for field in ['bid_amount', 'starting_price', 'item_name', 'description', 'watch_model', 'watch_reference_number', 'item_condition', 'auction_start', 'auction_deadline']:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])

    if not update_fields:
        return APIResponse("No update parameters provided", 400).to_flask_response()

    values.append(item_id)  # Append item_id for WHERE clause

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = f"UPDATE items SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(sql_query, tuple(values))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/delete_item', methods=['DELETE'])
def delete_item():
    """ Delete an item """
    data = request.get_json()
    item_id = data['item_id']

    if not item_id:
        return APIResponse("Missing parameters", 400)

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "DELETE FROM items WHERE item_id = %s"
    cursor.execute(sql_query, (item_id,))
    db_connection.commit()
    cursor.close()
    db_connection.close()
    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/get_item', methods=['GET'])
def get_item():
    """ Get an item by id """
    item_id = request.args.get('id')
    if not item_id:
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "SELECT * FROM items WHERE id = %s"
    cursor.execute(sql_query, (item_id,))
    item_data = cursor.fetchone()
    cursor.close()
    db_connection.close()
    # Format the auction_start and auction_deadline fields if they exist
    if 'auction_start' in item_data and item_data['auction_start']:
        item_data['auction_start'] = item_data['auction_start'].strftime(
            "%Y-%m-%d %H:%M:%S")
    if 'auction_deadline' in item_data and item_data['auction_deadline']:
        item_data['auction_deadline'] = item_data['auction_deadline'].strftime(
            "%Y-%m-%d %H:%M:%S")
    if item_data['item_image'] is not None:
        item_data['item_image'] = base64.b64encode(
            item_data['item_image']).decode('utf-8')
    if not item_data:
        return APIResponse("Item not found", 404).to_flask_response()
    return APIResponse(item_data, 200).to_flask_response()


@app.route('/api/item/search', methods=['GET'])
def search_items():
    search_query = request.args.get('query')
    if not search_query:
        return APIResponse("Missing search query", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    sql_query = "SELECT i.* FROM items i LEFT JOIN purchases p ON p.item_id = i.id WHERE p.item_id is NULL AND (item_name REGEXP %s OR description REGEXP %s OR brand REGEXP %s)"
    cursor.execute(sql_query, (search_query, search_query, search_query))
    results = cursor.fetchall()

    cursor.close()
    db_connection.close()
    for item in results:
        if item['item_image'] is not None:
            item['item_image'] = base64.b64encode(
                item['item_image']).decode('utf-8')
    return APIResponse(results, 200).to_flask_response()


@app.route('/api/item/filter_by_brand', methods=['GET'])
def filter_by_brand():
    brand_query = request.args.get('brand')
    if not brand_query:
        return APIResponse("Missing brand query", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    sql_query = "SELECT i.* FROM items i LEFT JOIN purchases p ON p.item_id = i.id WHERE p.item_id is NULL AND WHERE i.brand = %s"
    cursor.execute(sql_query, (brand_query,))
    results = cursor.fetchall()

    cursor.close()
    db_connection.close()

    for item in results:
        if item['item_image'] is not None:
            item['item_image'] = base64.b64encode(
                item['item_image']).decode('utf-8')
    return APIResponse(results, 200).to_flask_response()


@app.route('/api/item/add_brand', methods=['POST'])
def add_brand():
    data = request.get_json()
    brand_name = data['brand_name']

    if not brand_name:
        return APIResponse("Missing brand name", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "INSERT INTO brands (brand_name) VALUES (%s)"
    cursor.execute(sql_query, (brand_name,))
    db_connection.commit()
    brand_id = cursor.lastrowid
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/update_brand', methods=['POST'])
def update_brand():
    data = request.get_json()
    brand_id = data['brand_id']
    new_brand_name = data['new_brand_name']

    if not all([brand_id, new_brand_name]):
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "UPDATE brands SET brand_name = %s WHERE brand_id = %s"
    cursor.execute(sql_query, (new_brand_name, brand_id))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/delete_brand', methods=['DELETE'])
def delete_brand():
    data = request.get_json()
    brand_id = data['brand_id']

    if not brand_id:
        return APIResponse("Missing brand ID", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "DELETE FROM brands WHERE brand_id = %s"
    cursor.execute(sql_query, (brand_id,))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse(f"Successfully deleted brand ID {brand_id}", 200)


@app.route('/api/item/get_brands', methods=['GET'])
def get_brands():
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "SELECT * FROM brands"
    cursor.execute(sql_query)
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return APIResponse(results, 200).to_flask_response()


@app.route('/api/item/add_purchase', methods=['POST'])
def add_purchase():
    data = request.get_json()
    user_id = data['user_id']
    item_id = data['item_id']
    status = data['status']
    purchase_date = data['purchase_date']
    purchase_amount = data['purchase_amount']

    if not all([user_id, item_id, status, purchase_date, purchase_amount]):
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "INSERT INTO purchases (user_id, item_id, status, purchase_date, purchase_amount) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql_query, (user_id, item_id, status,
                   purchase_date, purchase_amount))
    db_connection.commit()
    purchase_id = cursor.lastrowid
    cursor.close()
    db_connection.close()

    return APIResponse({}, 200).to_flask_response()


@app.route('/api/item/update_purchase', methods=['POST'])
def update_purchase():
    data = request.get_json()
    itemIds = data['itemIds']
    print(data)
    print(itemIds)
    if not itemIds:
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    for itemId in itemIds:
        sql_query = "UPDATE purchases SET status = 'purchased' WHERE id = %s"
        cursor.execute(sql_query, (itemId,))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse(f"Success", 200).to_flask_response()


@app.route('/api/item/delete_purchase', methods=['DELETE'])
def delete_purchase():
    data = request.get_json()
    purchase_id = data['purchase_id']

    if not purchase_id:
        return APIResponse("Missing purchase ID", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "DELETE FROM user_purchases WHERE purchase_id = %s"
    cursor.execute(sql_query, (purchase_id,))
    db_connection.commit()
    cursor.close()
    db_connection.close()

    return APIResponse(f"Successfully deleted purchase ID {purchase_id}", 200).to_flask_response()


@app.route('/api/item/<int:user_id>/purchases', methods=['GET'])
def get_user_purchases(user_id):
    """
    Get all items that a user won
    """
    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)

    # SQL query to join the user_purchases and items tables
    sql_query = '''
    SELECT up.id, i.item_name, i.item_image, up.purchase_amount
    FROM items i
    INNER JOIN purchases up ON i.id = up.item_id
    WHERE up.user_id = %s AND status = "in-cart"
    '''

    cursor.execute(sql_query, (user_id,))
    purchases = cursor.fetchall()

    cursor.close()
    db_connection.close()

    for item in purchases:
        if item['item_image'] is not None:
            item['item_image'] = base64.b64encode(
                item['item_image']).decode('utf-8')
    return APIResponse(purchases, 200).to_flask_response()


@app.route('/api/item/get_purchase', methods=['GET'])
def get_purchase():
    """ Get a purchase by item id """
    item_id = request.args.get('item_id')
    if not item_id:
        return APIResponse("Missing parameters", 400).to_flask_response()

    db_connection = get_db_connection()
    cursor = db_connection.cursor(dictionary=True)
    sql_query = "SELECT * FROM purchases WHERE item_id = %s"
    cursor.execute(sql_query, (item_id,))
    item_data = cursor.fetchone()
    cursor.close()
    db_connection.close()
    if not item_data:
        return APIResponse("Item not found", 404).to_flask_response()
    # if item_data['item_image'] is not None:
    #     item_data['item_image'] = base64.b64encode(
    #         item_data['item_image']).decode('utf-8')
    return APIResponse(item_data, 200).to_flask_response()


# Add item to user_purchases.
# Frontend: Buy Now, Checkout
# Auction Microservice: Listen for messages from auction microservice to add item to user_purchases
#   build endpoint & rabbitmq consumer

if __name__ == "__main__":
    app.run(port=3901, debug=True, host='0.0.0.0')
