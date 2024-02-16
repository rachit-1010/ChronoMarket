from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, timedelta

# connect to database
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mysql",
    port=4099
)


app = Flask(__name__)
# port 3500 is the one we used for API Gateway
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})


class APIResponse:
    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_flask_response(self):
        return jsonify(self.data), self.status


@app.route('/api/auction', methods=['POST'])
def create_auction():
    """
    Create an auction on an item
    """
    data = request.get_json()
    user_id = data['user_id']
    email = data['user_email']
    item_id = data['id']
    item_name = data['item_name']
    start_time = data['auction_start']
    end_time = data['auction_deadline']

    # check if got all input
    if not all([user_id, email, item_id, item_name, start_time, end_time]):
        return APIResponse("Missing data", 400).to_flask_response()

    # Parse and format the start_time
    try:
        if 'T' in start_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        else:
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return APIResponse("Invalid start_time format", 400).to_flask_response()

    # insert data into auction mysql database
    with mysql_connection.cursor() as cursor:
        status = "live" if start_time < datetime.now() else "pending"
        sql = "INSERT INTO Auctions (user_id, email, item_id, item_name, start_time, end_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            sql, (user_id, email, item_id, item_name, start_time.strftime("%Y-%m-%d %H:%M:%S"), end_time, status))
        mysql_connection.commit()
    return APIResponse(f"Successfully Built Auction", 200).to_flask_response()


@app.route('/api/auction/status', methods=['GET'])
def get_auction_status():
    """
    Get an auction status
    """
    data = request.get_json()
    auction_id = data['auction_id']

    # check if got all input
    if not auction_id:
        return APIResponse("Missing data", 400).to_flask_response()

    # get auction status from mysql database
    with mysql_connection.cursor() as cursor:
        sql = "SELECT status FROM Auctions WHERE id = %s"
        cursor.execute(sql, (auction_id,))
        result = cursor.fetchone()

    return APIResponse({"status": result[0]}, 200).to_flask_response()


@app.route('/api/auction/live', methods=['GET'])
def get_live_auctions():
    """
    Get all live auctions
    """

    # get live auctions from mysql database
    with mysql_connection.cursor() as cursor:
        sql = "SELECT * FROM Auctions WHERE status = 'live'"
        cursor.execute(sql)
        results = cursor.fetchall()

    live_auctions = []
    for result in results:
        data = {'auction_id': result[0],
                'seller_id': result[1],
                'seller_email': result[2],
                'item_id': result[3],
                'item_name': result[4],
                'start_time': result[5],
                'end_time': result[6],
                'status': result[7]}
        live_auctions.append(data)

    return APIResponse({"live_auctions": live_auctions}, 200).to_flask_response()


@app.route('/api/auction/closed/count/<string:timeframe>', methods=['GET'])
def get_closed_auctions_count(timeframe):
    """
    Get the count of all closed auctions in a given timeframe
    """

    # calculate the start time based on the timeframe
    if timeframe == 'day':
        start_time = datetime.now() - timedelta(days=1)
    elif timeframe == 'week':
        start_time = datetime.now() - timedelta(weeks=1)
    elif timeframe == 'month':
        start_time = datetime.now() - timedelta(days=30)
    else:
        return APIResponse({"Invalid timeframe", 400}).to_flask_response()

    # get count of closed auctions from mysql database
    with mysql_connection.cursor() as cursor:
        sql = "SELECT COUNT(*) FROM Auctions WHERE status = 'closed' AND end_time >= %s"
        cursor.execute(sql, (start_time,))
        result = cursor.fetchone()

    return APIResponse({"closed_auctions_count": result[0]}, 200).to_flask_response()


@app.route('/api/auction/admin', methods=['POST'])
def admin_change_status():
    """
    Change an auction status
    """
    data = request.get_json()
    auction_id = data['auction_id']
    new_status = data['new_status']

    # check if got all input
    if not all([auction_id, new_status]):
        return APIResponse("Missing data", 400).to_flask_response()

    # update auction status in mysql database
    with mysql_connection.cursor() as cursor:
        if new_status == "live":
            sql = "UPDATE Auctions SET status = %s, start_time = %s WHERE id = %s"
        elif new_status == "closed":
            sql = "UPDATE Auctions SET status = %s, end_time = %s WHERE id = %s"
        else:
            pass
        cursor.execute(sql, (new_status, datetime.now(), auction_id))
        mysql_connection.commit()

    return APIResponse("Auction status changed", 200).to_flask_response()


@app.route('/api/auction/buy_now', methods=['POST'])
def buy_now_change_status():
    """
    Change an auction status
    """
    data = request.get_json()
    item_id = data['id']

    # check if got all input
    if not all([item_id]):
        return APIResponse("Missing data", 400).to_flask_response()

    # update auction status in mysql database
    with mysql_connection.cursor() as cursor:
        sql = "UPDATE Auctions SET status = %s, end_time = %s WHERE item_id = %s"
        cursor.execute(sql, ("closed", datetime.now(), item_id))
        mysql_connection.commit()

    return APIResponse("Auction status changed", 200).to_flask_response()


if __name__ == '__main__':
    app.run(port=4000, debug=True, host='0.0.0.0')
