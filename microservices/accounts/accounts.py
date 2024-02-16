import mysql.connector as mysql
from flask import Flask, request
import bcrypt
from datetime import datetime
import string
import random
from flask_cors import CORS

app= Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3500"}})
    
# ------------------------------ Class Definitions --------------------------------------
class APIResponse:
    """ Define a class for structuring API responses"""
    def __init__(self, data, status):
        self.data = data
        self.status = status

class Account:
    """ Define a generic accounts object with basic functions"""
    def __init__(self):  
        self.username = ""


    def login(self, username, password):
        """ Function for user login """
        user_query = execute_db_query('SELECT id, password, api_key, email, admin_account, suspended FROM users WHERE username = %s', (username,), one=True)

        # if username doesn't exist
        if not user_query:
            return APIResponse({"error": "User does not exist."}, 404)
        else:
            # get all the data
            db_hashed_password = user_query['password']
            api_token = user_query['api_key']
            admin_status = user_query['admin_account']
            suspended_status = user_query['suspended']
            email = user_query['email']
            user_id = user_query['id']

            # check if this email is blocked
            blocked_query = execute_db_query('SELECT blocked FROM blocked_users WHERE email = %s', (email,), one=True)
            if blocked_query:
                if blocked_query["blocked"] == 1:
                    return APIResponse({"error": "This user email address is blocked.", "status": "blocked"}, 401)

            # encode both passwords and compare
            password_bytes = password.encode('utf-8')
            db_hashed_password_bytes = db_hashed_password.encode('utf-8')

            # if password matches hash, must be the correct password and return api token and admin status
            if bcrypt.checkpw(password_bytes, db_hashed_password_bytes):
                # if user account is suspended
                if suspended_status == 1:
                    return APIResponse({"error": "This user account is suspended.", "api_key": api_token, "status": "suspended"}, 200)
                return APIResponse({"api_key": api_token, "email": email, "admin_status": admin_status, "user_id": user_id, "username": username}, 200)
            else:
                return APIResponse({"error": "Invalid password."}, 401)
    

    def register(self, admin_status, username, password, email):
        """ Function for user registration """
        # check if username already exists
        check_exists = execute_db_query("SELECT api_key FROM users WHERE username = %s", (username,), one=True)
        if check_exists is not None:
            return APIResponse({"error": "Username is already taken, please choose another.", "status": "duplicate"}, 400)
        
        # check if this email address is blocked
        blocked_query = execute_db_query('SELECT blocked FROM blocked_users WHERE email = %s', (email,), one=True)
        if blocked_query:
            if blocked_query["blocked"] == 1:
                return APIResponse({"error": "This user email address is blocked.", "status": "blocked"}, 401)
        # create the user and get their ID
        api_key = new_user(username, password, admin_status, email)
        user_id_query = execute_db_query('SELECT id FROM users WHERE api_key = %s', (api_key,), one=True)
        user_id = user_id_query["id"]
        return APIResponse({"api_key": api_key, "email": email, "admin_status": admin_status, "user_id": user_id, "username": username}, 200)


    def delete_account(self, api_key, username) -> bool:
        """ Function for a user deleting their own or admin deleting any account"""
        validate, current_username = validate_api_token(api_key)

        # check the user exists
        check_exists = execute_db_query("SELECT id FROM users WHERE username = %s", (username,), one=True)
        if not check_exists:
            return APIResponse({"error": "User does not exist."}, 404)
        if validate:
            # if user or admin is deleting their OWN account matching the API token
            if current_username == username:
                execute_db_query("DELETE FROM users WHERE username = %s", (username,), one=True)
                return APIResponse({}, 200)
            # if the user is an admin, they can delete any account
            else:
                # verify the api token making the request matches an admin token
                admin_query = execute_db_query('SELECT admin_account FROM users WHERE api_key = %s', (api_key,), one=True)
                if admin_query and admin_query['admin_account'] == 1:
                    execute_db_query("DELETE FROM users WHERE username = %s", (username,), one=True)
                    return APIResponse({}, 200)
                else:
                    return APIResponse({"error": "You do not have permission to delete this user."}, 401)
        else:
            return APIResponse({"error": "Invalid API token."}, 401)
        

    def suspend_account(self, api_key, suspended_status) -> bool:
        """ Function for a user to suspend or un-suspend their own account"""
        validate, _ = validate_api_token(api_key)
        if validate:
            # check that the account they're trying to suspend or unsuspend is their own
            execute_db_query("UPDATE users SET suspended = %s WHERE api_key = %s", (suspended_status, api_key), one=True)
            if suspended_status == 1:
                return APIResponse({"status": "suspended"}, 200)
            if suspended_status == 0:
                return APIResponse({"status": "unsuspended"}, 200)
        else:
            return APIResponse({"error": "Invalid API token."}, 401)
    

    def update_information(self, api_key, update_field: str, update_val: str):
        """ Function for a user to update their username or password """
        if update_field == "password" or update_field == "username":
            validate, username = validate_api_token(api_key)
            if validate:
                # if updating a users password, need to hash the new password
                if update_field == "password":
                    update_val = bcrypt.hashpw(update_val.encode('utf-8'), bcrypt.gensalt())
                execute_db_query("UPDATE users SET {} = %s WHERE api_key = %s".format(update_field), (update_val, api_key), one=True)
                return APIResponse({}, 200)
            else:
                return APIResponse({"error": "Invalid API token."}, 401) 
        else:
            return APIResponse({"error": "The user field you are trying to update doesn't exist."}, 401) 

class Admin(Account):
    """ Define a class for Administrators"""
    def __init__(self):
        super().__init__()
    

    def block_account(self, api_key, email):
        """ Function for an admin to permanently block any users with the associated email address"""
        validate, _ = validate_api_token(api_key)
        if validate:
            # check if this email address is already blocked
            blocked_query = execute_db_query('SELECT blocked FROM blocked_users WHERE email = %s', (email,), one=True)
            if not blocked_query:
                execute_db_query('INSERT INTO blocked_users (email, blocked) VALUES (%s, 1)', (email,), one=True)
            return APIResponse({}, 200)
        else:
            return APIResponse({"error": "Invalid API token."}, 401) 
        
    
    def get_blocked_users(self):
        """ Function for an admin to get list of all blocked email addresses"""
        output = execute_db_query('SELECT email FROM blocked_users')
        # blocked users exist  
        if output is not None:
            return APIResponse(output, 200)
        else:
            return APIResponse({"error": "No blocked users found"}, 404)


    def list_users(self):
        """ Function for an admin to get a list of all non-admin users """
        output = execute_db_query('SELECT id, username, email FROM users WHERE admin_account = 0')
        # this user exists
        if output is not None:
            return APIResponse(output, 200)
        else:
            return APIResponse({"error": "No users found"}, 404)


class User(Account):
    """ Define a class for normal Users"""
    def __init__(self):
        super().__init__()


    def get_user_info(self, seller_id):
        """ Function to get a users email and username based on ID """
        output = execute_db_query('SELECT username, email FROM users WHERE id = %s', (seller_id, ), one=True)
        if output is not None:
            return APIResponse({"seller_email": output["email"], "seller_username": output["username"]}, 200)
        else:
            return APIResponse({"error": "This user was not found."}, 404)
    

    def add_to_watchlist(self, api_key, email, reference_num):
        """ Function for user adding an item to their watchlist """
        # check if this user already is watching this item
        check_duplicate = execute_db_query('SELECT * FROM watchlist WHERE watchlist_item = %s AND api_key = %s', (reference_num, api_key), one=True)
        if not check_duplicate:
            execute_db_query('INSERT INTO watchlist (api_key, email, watchlist_item) VALUES (%s, %s, %s)', (api_key, email, reference_num), one=True)
            return APIResponse({}, 200)
        else:
            # user is already watching this item
            return APIResponse({}, 204)


    def get_watchlist(self, reference_num):
        """ Get all users that have a specific watch reference number on their watchlist """
        output = execute_db_query('SELECT * FROM watchlist WHERE watchlist_item = %s', (reference_num,))
        # users are watching this item/reference number
        if output is not None:
            return APIResponse(output, 200)
        else:
            return APIResponse({"error": "No users found watching that item"}, 404)


# ------------------------------ Database Functions --------------------------------------
def connect_db():
    """ Function to connect to MySQL database hosted in Docker container """
    cnx = mysql.connect(
        user='user', 
        password='password', 
        database='mysql',
        host='localhost', 
        port=3406
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


# ------------------------------ Helper Functions --------------------------------------
def new_user(username: str, password: str, admin_status: int, email: str):
    """Function to create a new user in the database"""
    # generate an API key
    api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
    # hash and salt password and store in database
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    execute_db_query('INSERT INTO users (username, password, email, api_key, admin_account, suspended)' +
        'VALUES (%s, %s, %s, %s, %s, %s)', (username, hashed_pw, email, api_key, admin_status, 0), one=True)
    return api_key


def validate_api_token(request_token) -> (bool, str):
    """ Function to valid if a user provides a valid API token"""
    search_user = execute_db_query('SELECT username FROM users where api_key = %s', (request_token,), one=True)
    # if API token doesn't exist
    if search_user is None:
        return False, ""
    else:
        username = search_user['username']
        return True, username


# -------------------------------- API Signup/Login ROUTES ----------------------------------
@app.route('/api/accounts/validate', methods=['GET'])
def validate_token():
    """ Validate a users API token """  
    request_api_token = request.headers.get('Authorization')
    validate, _ = validate_api_token(request_api_token)
    # valid API token
    if validate:
        return ({}, 200)
    else:
        return ({"error": "Invalid API token."}, 401)


@app.route('/api/accounts/login', methods=['POST'])
def user_login():
    """ Login endpoint for users and admins"""  
    request_body = request.get_json()
    username = request_body.get('username')
    passw = request_body.get('password')

    # create User instance and login the user
    user_account = Account()
    api_response = user_account.login(username, passw)
    return api_response.data, api_response.status


@app.route('/api/accounts/admin/register', methods=['POST'])
def admin_sign_up():
    """ Sign up endpoint that creates a new admin and API token """
    request_body = request.get_json()
    username = request_body.get('username')
    passw = request_body.get('password')
    email = request_body.get('email')

    # create Admin instance and register them
    admin = Admin()
    api_response = admin.register(1, username, passw, email)
    return api_response.data, api_response.status


@app.route('/api/accounts/user/register', methods=['POST'])
def user_sign_up():
    """ Sign up endpoint that creates a new user and API token """
    request_body = request.get_json()
    username = request_body.get('username')
    passw = request_body.get('password')
    email = request_body.get('email')
    
    # create User instance and register the user
    user = User()
    api_response = user.register(0, username, passw, email)
    return api_response.data, api_response.status


# -------------------------------- API Account Action ROUTES ----------------------------------
@app.route('/api/accounts/user/email/<seller_id>', methods=['GET'])
def get_user_email(seller_id):
    """ Get a users email address """  
    user_account = User()
    api_response = user_account.get_user_info(seller_id)
    return api_response.data, api_response.status


@app.route('/api/accounts/update', methods=['POST'])
def update_user_info():
    """ Update the username, or password for a user """  
    request_body = request.get_json()
    request_api_token = request.headers.get('Authorization')
    field_to_update = request_body.get('update_type')
    value_to_update = request_body.get('update_value')

    user_account = Account()
    api_response = user_account.update_information(request_api_token, field_to_update, value_to_update)
    return api_response.data, api_response.status


@app.route('/api/accounts/user/suspend', methods=['POST'])
def suspend_account():
    """ Suspend a user account - can only be done by a user """  
    request_api_token = request.headers.get('Authorization')

    # create User instance and suspend the user
    user = User()
    api_response = user.suspend_account(request_api_token, 1)
    return api_response.data, api_response.status


@app.route('/api/accounts/user/unsuspend', methods=['POST'])
def unsuspend_account():
    """ Un-suspend a user account - can only be done by a user """  
    request_api_token = request.headers.get('Authorization')

    # create User instance and unsuspend the user
    user = User()
    api_response = user.suspend_account(request_api_token, 0)
    return api_response.data, api_response.status


@app.route('/api/accounts/admin/list', methods=['GET'])
def get_users():
    """ Get all users for admins to view """
    # create Admin instance and get all users
    admin = Admin()
    api_response = admin.list_users()
    return api_response.data, api_response.status


@app.route('/api/accounts/delete', methods=['POST'])
def delete_account():
    """ Delete a user account - can be done by a user to their own account, or by an admin to any user """  
    request_body = request.get_json()
    request_api_token = request.headers.get('Authorization')
    username = request_body.get('username')

    # create User instance and unsuspend the user
    account = Account()
    api_response = account.delete_account(request_api_token, username)
    return api_response.data, api_response.status


@app.route('/api/accounts/admin/block', methods=['POST'])
def block_user():
    """ An admin can permanently block an email address from being able to login or register an account """  
    request_body = request.get_json()
    request_api_token = request.headers.get('Authorization')
    email = request_body.get('email')

    # create Admin instance and block the user
    admin = Admin()
    api_response = admin.block_account(request_api_token, email)
    return api_response.data, api_response.status


@app.route('/api/accounts/admin/get_blocked', methods=['GET'])
def list_blocked_users():
    """ An admin can get all blockex users """  
    # create Admin instance and block the user
    admin = Admin()
    api_response = admin.get_blocked_users()
    return api_response.data, api_response.status


@app.route('/api/accounts/watchlist/<reference_num>', methods=['GET'])
def get_watchlist_users(reference_num):
    """ Get all users that have this item on their watchlist """  
    # create User instance and get all users that are watching this reference num
    user = User()
    api_response = user.get_watchlist(reference_num)

    return api_response.data, api_response.status


@app.route('/api/accounts/watchlist/add', methods=['POST'])
def add_watchlist():
    """ Add a user-watchlist combination """  
    request_body = request.get_json()
    request_api_token = request.headers.get('Authorization')
    reference_number = request_body.get('reference_num')
    email = request_body.get('email')

    # create User instance and add this user/reference number combo to watchlist data
    user = User()
    api_response = user.add_to_watchlist(request_api_token, email, reference_number)
    return api_response.data, api_response.status


# run accounts Flask service on port 3900
if __name__ == "__main__":
    app.run(port=3900, debug=True, host='0.0.0.0')