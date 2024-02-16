from flask import Flask, request, jsonify
import redis
import json
import mysql.connector as mysql
from datetime import datetime
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})

# r = redis.Redis()


class APIResponse:
    """ Irrigated from accounts.py"""
    def __init__(self, data, status):
        self.data = data
        self.status = status

    def to_flask_response(self):
        return jsonify(self.data), self.status


# Ashkan => list of tuples (of user_id, and user_email)
@app.route('/api/notifications/auction_end', methods= ['POST'])
def auction_end():
    """
    send an email to all the bidders and the seller
    that the auction window is closed.
    """
    data = request.get_json()
    print("data: ",data)

    
    email = data.get("email")
    ### update  in sync####
    item_name = data.get("auction")
    ### update ####

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # auction_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"The auction: {item_name} has ended!"
    email_body = f'''
    <html>
        <body>
            <p>The auction: {item_name} has been closed</p>
            <br>
            <p>To Buyers: The winner of the auction has been notified via a separate email!</p>
            <br>
            <p>To Seller: Your auction has a winner! The item is now in their shopping cart</p>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200


@app.route('/api/notifications/watchlist', methods= ['POST'])
def watchlist_item_notification():
    """
    notify users when an item that matches their watchlist criteria
    is listed for auction
    """
    data = request.get_json()
    print("data: ",data)

    
    email = data.get("email")
    ### update  in sync####
    item_name = data.get("item")
    ### update ####

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # item_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"Watch list alert!"
    email_body = f'''
    <html>
        <body>
            <p>The item with the following reference number: {item_name} that matches your Watch List has been listed for auction!</p>
            <br>
            <p>Please submit a bid to participate in this auction!</p>
            <br>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200


# receive one dictionary at a time => from Ashkan 
@app.route('/api/notifications/high_bid', methods = ['POST'])
def new_high_bid():
    """
    notify the previous high bidder that they were outbid
    """
    data = request.get_json()
    print("data: ",data)

    
    email = data.get("email")
    ### update  in sync####
    item_name = data.get("auction")
    ### update ####

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # auction_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"You have been out-bid for the auction: {item_name}"
    email_body = f'''
    <html>
        <body>
            <p>your previous high-bid for auction: {item_name} has been out-bid</p>
            <br>
            <p>Please submit a new bid higher than the current high-bid to secure your auction-win</p>
            <br>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200



@app.route('/api/notifications/one_hour', methods = ['POST'])
def one_hour():
    """
    notify (send an email) to all the bidders on an item and the seller
    that the auction ends in 1 hour
    """
    data = request.get_json()
    print("data: ",data)

    
    email = data.get("email")
    ### update  in sync####
    item_name = data.get("auction")
    ### update ####

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # auction_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"One-Hour Alert for the Auction: {item_name}"
    email_body = f'''
    <html>
        <body>
            <p>The Auction: {item_name} ends in 1 hour!</p>
            <br>
            <p>To Buyers: This is the final reminder for the auction! Please re-evaluate your bids to be the grand-winner!</p>
            <p>To Seller: your patience is paying off. One more hour to go! :D </p>
            <br>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200


@app.route('/api/notifications/one_day', methods = ['POST'])
def one_day():
    """
    notify (send an email) to all bidders on an item and the seller
    that the auction ends in 1 day
    """


    data = request.get_json()
    print("data: ",data)

    
    email = data.get("email")
    ### update  in sync####
    item_name = data.get("auction")
    ### update ####

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # auction_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"One-Day Alert for the Auction: {item_name}"
    email_body = f'''
    <html>
        <body>
            <p>The Auction: {item_name} ends in 1 day!</p>
            <br>
            <p>To Buyers: stay tuned!, we will notify you once more when the auction ends in 1 hour!</p>
            <p>To Seller: your auction will have a grand-winner in 1 day! :D </p>
            <br>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200


@app.route('/api/notifications/winning_bid', methods = ['POST'])
def winning_bid():
    """
    notify (send an email) the user who had the final-high bid on the auction
    when the auction ends
    """
    data = request.get_json()

    # finalize
    email = data.get("email")
    item_name = data.get("auction")

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com', 'arohani@uchicago.edu']
    # auction_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"CONGRATULATIONS You have won the auction: {item_name}"
    email_body = f'''
    <html>
        <body>
            <p>>Your bid for the auction: {item_name} has been finalized</p>
            <br>
            <p>You are the winner of the auction! The item has been added to your shopping cart.</p>
            <p>You can checkout from the shopping cart whenever you wish.</p>
            <br>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200


@app.route('/api/notifications/seller_new_bid', methods = ['POST'])
def seller_new_bid():
    """
    notify the seller about a new bid on their auction
    """
    data = request.get_json()

    # finalize
    email = data.get("email")
    item_name = data.get("auction")

    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email


    # # testing with placeholder
    # recipients = ['esegerberg@uchicago.edu', 'bigcheddarchees@gmail.com']
    # auction_name = "Hazzah"
    # # testing with placeholder


    email_subject = f"Your auction: {item_name} has a new bid!"
    email_body = f'''
    <html>
        <body>
            <p>>Your auction: {item_name} has a new bid!</p>
            <br>
            <p>Go check it out on our website! :D</p>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, email_subject, email_body)
    return {}, 200

    


# outlook smtp version
def send_email(recipients, email_subject, email_body):
    """
    to send emails based on the email addresses that I obtained

    """
    # email_rdy = MIMEText(email_body)
    
    sender_email = "chronomarket@outlook.com"
    pw = "qwerty@12345P"

    # start SMTP session
    smtp = smtplib.SMTP("smtp-mail.outlook.com", 587)
    smtp.starttls()
    smtp.login(sender_email, pw)



    email_rdy = MIMEMultipart("alternative")
    email_rdy['From'] = sender_email
    email_rdy["Subject"] = email_subject
    
    #printing out recipients
    print("recipients: ", recipients)

    
    ## CHECK 
    email_rdy['To'] = ', '.join(recipients)
    email_rdy.attach(MIMEText(email_body, "html"))

    # TO list check-up
    print("To list(converted to send-mode): ", email_rdy['To'])
    
    print("recipients_list: ", recipients)

    try:
        smtp.sendmail(sender_email, recipients, email_rdy.as_string())
        print("emails have been sent")

    except Exception as doom:
        print("doom: ", doom)


    smtp.quit()

        



# customer support => one get endpoint, one post endpoint (acquiring customer feedback, posting email reponses from admin)
@app.route('/api/notifications/respond_feedback', methods = ['POST'])
def customer_support():
    data = request.get_json()
    email = data.get("email")
    recipients = []

    if type(email) == str:
        recipients.append(email)
    elif type(email) == list:
        recipients = email

    subject = data.get("subject")
    body = data.get("body")
    username = data.get("username")


    email_body = f'''
    <html>
        <body>
            <p>Dear User {username}, </p> 
            <br> 
            <p>{body}</p>
            
            <br>
            <br>
            <p>Sincerely, ChronoMarkets</p>
            <br>
            <p>This is an automated email. Please don't respond to this email</p>

        </body>
    </html>
    '''

    send_email(recipients, subject, email_body)
    return {}, 200



# add a single user feedback
@app.route('/api/notifications/add_feedback',methods = ['POST'])
def add_one_feedback():
    try:
        data = request.get_json()
        print("data: ",data)

        username = data.get("username")
        email = data.get("email")
        feedback_body = data.get("feedback_body")

        execute_db_query("INSERT INTO feedback (username, email, feedback_body) VALUES (%s, %s, %s)", (username, email, feedback_body), one = True)

        return APIResponse({"message": "Feedback has been successfully added to DB"}, 200).to_flask_response()

    except Exception as doom:

        return APIResponse({"insert has doomed": doom}, 500).to_flask_response()

        


# getting all feedbacks
@app.route('/api/notifications/list_all_feedback', methods = ['GET'])
def list_all_feedback():
    
    result = execute_db_query("SELECT * FROM feedback WHERE responded_to = 0")

    if result is None:
        return APIResponse({"error": "We have no Feedback :( "}, 404).to_flask_response()

    return APIResponse(result, 200).to_flask_response()



# responding to a feedback
@app.route('/api/notifications/update_feedback', methods = ['PUT'])
def update_feedback():
    try:

        data = request.get_json()

        feedback_id = data.get("feedback_id")


        execute_db_query("UPDATE feedback SET responded_to = 1 WHERE id = %s", (feedback_id,))

        return APIResponse({"message": f"You have successfully replied to the feedback! with id: {feedback_id}"}, 200).to_flask_response()

    except Exception as doom:

        return APIResponse({"update has doomed": doom}, 500).to_flask_response()

   


## check port
def connect_db():
    """ Function to connect to MySQL database hosted in Docker container """
    cnx = mysql.connect(
        user='user', 
        password='password', 
        database='mysql',
        host='localhost', 
        port=7887
    )
    return cnx


def execute_db_query(query, args=(), one=False):
    """ Function to perform sanitized database queries """
    db_cnx = connect_db()
    cursor = db_cnx.cursor(dictionary=True)
    cursor.execute(query, args)

    if query.lower().startswith("select"):
        rows = cursor.fetchall()
    else:
        rows = None

    db_cnx.commit()
    cursor.close()
    if rows:
        if one:
            return rows[0]
        return rows
    return None



if __name__ == "__main__":
    # run notifications Flask service on port 7777
    app.run(port=7777, debug=True, host='0.0.0.0')



 









  
