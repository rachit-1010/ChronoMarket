from datetime import datetime, timedelta
import requests
import time
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
import socket

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)


# connect to database
mysql_connection = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mysql",
    port=4099
)


def auto_change_auction_status():
    """
    Check all auctions and update their status based on the current time
    """
    print("Checking auction status...")

    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)
    one_hour_one_minute_later = one_hour_later + timedelta(minutes=1)
    print("now", now)
    print("one_hour_later", one_hour_later)
    headers = {
        "Content-Type": "application/json"
    }

    # update auction status in mysql database
    with mysql_connection.cursor() as cursor:

        # start auctions
        sql = "UPDATE Auctions SET status = 'live' WHERE start_time <= %s AND status = 'pending'"
        cursor.execute(sql, (now,))

        # message 2: one hour
        # get auctions that will end in one hour
        sql = "SELECT * FROM Auctions WHERE end_time < %s AND end_time >= %s AND status = 'live'"
        cursor.execute(sql, (one_hour_one_minute_later, one_hour_later,))
        auctions_ending_soon = cursor.fetchall()

        # send message for each auction ending soon
        for auction in auctions_ending_soon:
            data = {'data': {'auction_id': auction[0],
                             'seller_id': auction[1],
                             'seller_email': auction[2],
                             'item_id': auction[3],
                             'item_name': auction[4],
                             'notifications': 'one_hour'},
                    'topic': 'request.bidding.emails'}
            response = requests.post(
                f'http://{host_ip}:3750/api/message_broker', json=data, headers=headers)
            if response.status_code == 200:
                print(f" [x] Sent request.bidding.emails, one_hour:{auction}")
            else:
                print(
                    f" [!] Failed to send message for auction, one_hour: {auction}")

        # end auctions
        sql = "UPDATE Auctions SET status = 'closed' WHERE end_time <= %s AND status != 'closed'"
        cursor.execute(sql, (now,))

        # message 3: end auctions
        sql = "SELECT * FROM Auctions WHERE end_time <= %s AND end_time > %s AND status = 'closed'"
        cursor.execute(sql, (now, now - timedelta(seconds=60),))
        auctions_just_ended = cursor.fetchall()

        # send message for each auction just ended
        for auction in auctions_just_ended:
            data = {'data': {'auction_id': auction[0],
                             'seller_id': auction[1],
                             'seller_email': auction[2],
                             'item_id': auction[3],
                             'item_name': auction[4],
                             'notifications': 'auction_end'},
                    'topic': 'request.bidding.emails'}
            response = requests.post(
                f'http://{host_ip}:3750/api/message_broker', json=data, headers=headers)
            if response.status_code == 200:
                print(
                    f" [x] Sent request.bidding.emails, auction_end,:{auction}")
            else:
                print(
                    f" [!] Failed to send message for auction, auction_end: {auction}")

        mysql_connection.commit()

    print("Auction status checked.")


# create scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=auto_change_auction_status,
                  trigger="interval", seconds=60)
scheduler.start()

# Keep the script running.
while True:
    time.sleep(1)
