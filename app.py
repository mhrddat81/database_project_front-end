import random
from flask import Flask, render_template, request, jsonify, send_from_directory
import mysql.connector
from faker import Faker
from datetime import datetime

database_name = "exchangeManagement"
admins = {"admin": "admin123", "report": "report123", "usermanager": "usermanager123"}

root_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ُشمشیثناهغشق1382",
    database=database_name
)

cursor = root_db.cursor()

# region user creation queries
# cursor.execute("""CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin123'""")
# cursor.execute(f"""GRANT ALL PRIVILEGES ON {database_name}.* TO 'admin'@'localhost'""")
#
# cursor.execute("""CREATE USER IF NOT EXISTS 'report'@'localhost' IDENTIFIED BY 'report123'""")
# cursor.execute(f"""GRANT SELECT ON {database_name}.* TO 'report'@'localhost'""")
#
# cursor.execute("""CREATE USER IF NOT EXISTS 'usermanager'@'localhost' IDENTIFIED BY 'usermanager123'""")
# cursor.execute(f"""GRANT ALL PRIVILEGES ON {database_name}.users TO 'usermanager'@'localhost'""")

# cursor.execute("""CREATE USER IF NOT EXISTS 'user'@'localhost' IDENTIFIED BY 'user123'""")
# cursor.execute(f"""GRANT SELECT, INSERT, UPDATE, DELETE ON {database_name}.* TO 'user'@'localhost'""")

# region Initial Queries

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

# region Tables Creation

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
    UserID bigint NOT NULL PRIMARY KEY,
    Username char(30) NOT NULL UNIQUE,
    UserPassword char(30) NOT NULL,
    FirstName char(30),
    LastName char(30),
    Address char(100),
    Email char(40))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Wallet(
    WalletID bigint NOT NULL PRIMARY KEY,
    UserID bigint NOT NULL,

    FOREIGN KEY(UserID)
    REFERENCES Users(UserID)
    ON DELETE CASCADE
    ON UPDATE CASCADE)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Currency(
    CurrencyCode char(3) NOT NULL PRIMARY KEY,
    CurrencyName char(20) NOT NULL)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS WalletCurrency(
        WalletID bigint NOT NULL,
        CurrencyCode char(3) NOT NULL,
        Amount float,
        
        PRIMARY KEY(WalletID, CurrencyCode),
        
        FOREIGN KEY(WalletID)
        REFERENCES Wallet(WalletID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
        FOREIGN KEY(CurrencyCode)
        REFERENCES Currency(CurrencyCode)
        ON DELETE CASCADE
        ON UPDATE CASCADE)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Market(
    MarketID bigint NOT NULL PRIMARY KEY,
    MarketName char(40) NOT NULL,
    BaseCurrencyCode char(3),
    TargetCurrencyCode char(3),
    ExchangeAmount float,
    
    FOREIGN KEY(BaseCurrencyCode)
    REFERENCES Currency(CurrencyCode)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    
    FOREIGN KEY(TargetCurrencyCode)
    REFERENCES Currency(CurrencyCode)
    ON DELETE SET NULL
    ON UPDATE CASCADE)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS UserTransaction(
    TranscationID bigint NOT NULL PRIMARY KEY,
    UserID bigint,
    MarketID bigint,
    PaidAmount float NOT NULL,
    BoughtAmount float NOT NULL,
    TransactionDate datetime,
    
    FOREIGN KEY(UserID)
    REFERENCES Users(UserID)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    
    FOREIGN KEY(MarketID)
    REFERENCES Market(MarketID)
    ON DELETE SET NULL
    ON UPDATE CASCADE)""")

# endregion

# endregion

# region Random data generation

fake = Faker()

# for userID in range(1, 1000):
#     query = """UPDATE Users SET Username = %s WHERE UserID = %s"""
#     username = fake.user_name()
#
#     cursor.execute("""SELECT UserID FROM Users WHERE Username = %s""", (username,))
#
#     if cursor.fetchall():
#         while cursor.fetchall():
#             username = fake.user_name()
#             cursor.execute("""SELECT UserID FROM Users WHERE Username = %s""", (username,))
#
#     val = (username, userID)
#     cursor.execute(query, val)
#     root_db.commit()

# for userID in range(1, 1000):
#     query = """INSERT INTO Users (UserID, UserPassword, FirstName, LastName, Address, Email)
#      VALUES (%s, %s, %s, %s, %s, %s)"""
#     val = (userID, fake.password(), fake.first_name(), fake.last_name(), fake.address(), fake.email())
#     cursor.execute(query, val)
#     root_db.commit()

# for walletID in range(1, 3000):
#     query = """INSERT INTO Wallet (WalletID, UserID)
#      VALUES (%s, %s)"""
#     val = (walletID, fake.random_int(min=1, max=999))
#     cursor.execute(query, val)
#     root_db.commit()

# cursor.execute("""INSERT INTO Currency (CurrencyCode, CurrencyName)
#  VALUES ('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'Pound Sterling'), ('JPY', 'Japanese Yen'),
#  ('IRR', 'Iranian Rial'), ('CAD', 'Canadian Dollar'), ('AUD', 'Australian Dollar'), ('CHF', 'Swiss Franc'),
#  ('RUB', 'Russian Ruble'), ('CNY', 'Chinese Yuan'), ('TRY', 'Turkish Lira'), ('NZD', 'New Zealand Dollar'),
#  ('SEK', 'Swedish Krona'), ('BRL', 'Brazilian Real'), ('INR', 'Indian Rupee'), ('ZAR', 'South African Rand')""")
# root_db.commit()

# for i in range(1, 10000):
#     query_select = "SELECT WalletID, CurrencyCode FROM WalletCurrency WHERE WalletID = %s AND CurrencyCode = %s"
#     query_insert = "INSERT INTO WalletCurrency (WalletID, CurrencyCode, Amount) VALUES (%s, %s, %s)"
#
#     currencyCode = fake.random_element(elements=('USD', 'EUR', 'GBP', 'JPY', 'IRR', 'CAD', 'AUD', 'CHF', 'RUB', 'CNY',
#                                                  'TRY', 'NZD', 'SEK', 'BRL', 'INR', 'ZAR'))
#     walletID = fake.random_int(min=1, max=2999)
#
#     cursor.execute(query_select, (walletID, currencyCode))
#     fetch = cursor.fetchall()
#
#     while fetch:
#         walletID = fake.random_int(min=1, max=2999)
#         cursor.execute(query_select, (walletID, currencyCode))
#         fetch = cursor.fetchall()
#
#     val = (walletID, currencyCode, fake.random_int(min=1, max=100000))
#     cursor.execute(query_insert, val)
#     root_db.commit()

# marketID = 1
# for base in ('USD', 'EUR', 'GBP', 'JPY', 'IRR', 'CAD', 'AUD', 'CHF', 'RUB', 'CNY', 'TRY', 'NZD', 'SEK', 'BRL', 'INR', 'ZAR'):
#     for target in ('USD', 'EUR', 'GBP', 'JPY', 'IRR', 'CAD', 'AUD', 'CHF', 'RUB', 'CNY', 'TRY', 'NZD', 'SEK', 'BRL', 'INR', 'ZAR'):
#         if base != target:
#             query = """INSERT INTO Market (MarketID, MarketName, BaseCurrencyCode, TargetCurrencyCode, ExchangeAmount)
#                 VALUES (%s, %s, %s, %s, %s)"""
#             cursor.execute("SELECT ExchangeAmount FROM Market"
#                            " WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s", (target, base))
#             fetch = cursor.fetchall()
#             if not fetch:
#                 exchangeAmount = random.uniform(0.5, 100000)
#             else:
#                 exchangeAmount = 1 / fetch[0][0]
#             val = (marketID, base + '/' + target, base, target, exchangeAmount)
#             cursor.execute(query, val)
#             root_db.commit()
#             marketID += 1


# for transactionID in range(1, 10000):
#     query = """INSERT INTO UserTransaction (TranscationID, UserID, MarketID, PaidAmount, BoughtAmount, TransactionDate)
#      VALUES (%s, %s, %s, %s, %s, %s)"""
#     cursor.execute("SELECT UserID FROM Users")
#     fetch = cursor.fetchall()
#     userID = random.choice(fetch)[0]
#     cursor.execute("SELECT MarketID FROM Market")
#     fetch = cursor.fetchall()
#     marketID = random.choice(fetch)[0]
#     cursor.execute("SELECT ExchangeAmount FROM Market WHERE MarketID = %s", (marketID,))
#     fetch = cursor.fetchall()
#     exchangeAmount = fetch[0][0]
#     paidAmount = random.uniform(0.5, 100000)
#     boughtAmount = paidAmount * exchangeAmount
#     start_date = datetime(2015, 1, 1)
#     end_date = datetime(2023, 12, 31)
#     val = (transactionID, userID, marketID, paidAmount, boughtAmount, fake.date_time_between_dates(start_date, end_date))
#     cursor.execute(query, val)
#     root_db.commit()


# endregion

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    data = request.json
    userid = data.get('userid')
    query_user = "SELECT Username, Firstname, Lastname FROM Users WHERE UserID = %s"
    query_transaction = """SELECT PaidAmount, BoughtAmount, TransactionDate, MarketName
        FROM UserTransaction, Market WHERE UserTransaction.UserID = %s
         AND UserTransaction.MarketID = Market.MarketID"""
    query_wallet = """SELECT CurrencyCode, Amount FROM WalletCurrency
        WHERE WalletID IN (SELECT WalletID FROM Wallet WHERE UserID = %s)"""

    cursor.execute(query_user, (userid,))
    user = cursor.fetchone()

    cursor.execute(query_transaction, (userid,))
    transaction = cursor.fetchall()

    cursor.execute(query_wallet, (userid,))
    wallet = cursor.fetchall()

    return jsonify(userinfo=user, transactioninfo=transaction, walletinfo=wallet)


@app.route('/trade')
def trade():
    return render_template('trade_window.html')


@app.route('/confirm_trade')
def confirm_trade():
    data = request.json
    userid = data.get('userid')
    base_currency = data.get('base_currency')
    target_currency = data.get('target_currency')
    target_amount = data.get('target_amount')

    # check if user has enough base currency in his wallet
    query = """SELECT Amount FROM WalletCurrency
        WHERE WalletID IN (SELECT WalletID FROM Wallet WHERE UserID = %s)
        AND CurrencyCode = %s"""
    cursor.execute(query, (userid, base_currency))
    fetch = cursor.fetchone()
    base_amount = fetch[0]

    query = """SELECT ExchangeAmount FROM Market
        WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s"""
    cursor.execute(query, (base_currency, target_currency))
    fetch = cursor.fetchone()
    exchange_amount = fetch[0]

    if base_amount >= target_amount * exchange_amount:
        # update user wallet
        query = """UPDATE WalletCurrency SET Amount = Amount - %s
            WHERE WalletID IN (SELECT WalletID FROM Wallet WHERE UserID = %s)
            AND CurrencyCode = %s"""
        cursor.execute(query, (target_amount * exchange_amount, userid, base_currency))
        root_db.commit()

        query = """UPDATE WalletCurrency SET Amount = Amount + %s
            WHERE WalletID IN (SELECT WalletID FROM Wallet WHERE UserID = %s)
            AND CurrencyCode = %s"""
        cursor.execute(query, (target_amount, userid, target_currency))
        root_db.commit()

        # add transaction to user transaction history
        query = """INSERT INTO UserTransaction (UserID, MarketID, PaidAmount, BoughtAmount, TransactionDate)
            VALUES (%s, (SELECT MarketID FROM Market WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s), %s, %s, %s)"""
        cursor.execute(query, (
        userid, base_currency, target_currency, target_amount * exchange_amount, target_amount, datetime.now()))
        root_db.commit()

        return jsonify(success=True)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')


# @app.route('/process_recovery', methods=['POST'])
# def process_recovery():
#     data = request.json
#     email = data.get('email')
#
#     # Add logic to send recovery email
#     # For demonstration purposes, let's assume the email is sent successfully
#     # In a real application, you would send an email with a unique link for password reset
#
#     return jsonify(success=True)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    entered_username = data.get('username')
    entered_password = data.get('password')

    if entered_username in admins.keys() and entered_password == admins[entered_username]:
        return jsonify(success=True, role=entered_username)
    else:
        query = """SELECT UserID FROM Users WHERE Username = %s"""
        cursor.execute(query, (entered_username,))
        fetch = cursor.fetchall()
        if fetch:
            return jsonify(success=True, role='user')


@app.route('/get_user_profile_data')
def get_user_profile_data():
    # Replace this with your actual logic to fetch user profile data from the server
    user_profile_data = {
        'name': 'John Doe',
        'profilePic': 'profile-pic.jpg',
        # Add more profile data as needed
    }
    return jsonify(user_profile_data)


@app.route('/get_assets_data')
def get_assets_data():
    # Replace this with your actual logic to fetch dynamic asset data from the server
    assets_data = [
        {'name': 'Asset 1', 'value': 1000},
        {'name': 'Asset 2', 'value': 500},
        # Add more assets as needed
    ]
    return jsonify(assets_data)


@app.route('/cancel_trade', methods=['POST'])
def cancel_trade():
    # Implement logic to cancel the trade (if needed)

    # For now, let's assume the trade was canceled successfully
    # Replace this with your actual cancellation logic
    success = True

    return jsonify({'success': success})


@app.route('/submit_purchase', methods=['POST'])
def submit_purchase():
    try:
        # Get data from the request
        data = request.get_json()
        currency = data['currency']
        amount = data['amount']
        transaction_type = data['type']

        # Get current date and time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Calculate the total based on your logic (replace this with your actual price)
        # For simplicity, let's assume a fixed price for each transaction
        price_per_unit = 1.5  # Replace with your actual price
        total = price_per_unit * amount

        # Create a new transaction entry
        new_transaction = {
            'transaction': currency,
            'amount': amount,
            'status': transaction_type,
            'total': total,
            'date': current_date,
            'time': current_time
        }

        # Assuming you have a global list 'transaction_history' to store transaction data
        # transaction_history.append(new_transaction)

        # Return a success response
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/get_transaction_history_data')
def get_transaction_history_data():
    # Replace this with your actual logic to fetch transaction history data from the server
    transaction_history_data = [
        {'transaction': 'USD', 'amount': 200, 'status': 'buy', 'total': 1200, 'date': '2022-03-01', 'time': '14:30'},
        {'transaction': 'IRR', 'amount': 100000000, 'status': 'sell', 'total': 1100, 'date': '2022-03-02',
         'time': '10:45'},
        # Add more transaction history entries as needed
    ]
    return jsonify(transaction_history_data)


@app.route('/edit_profile', methods=['POST'])
def edit_profile():
    try:
        # Get form data from the request
        data = request.form
        profile_image = request.files['profileImage']  # Handle file upload if needed
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        phone_number = data['phoneNumber']
        dob = data['dob']

        # Implement logic to update the user's profile (replace this with your logic)
        # ...

        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# region default queries


@app.route('/get_user_wallet_balances/<int:userID>')
def get_user_wallet_balances(userID):
    query = """SELECT CurrencyCode, Amount FROM WalletCurrency
    WHERE WalletID IN (SELECT WalletID FROM Wallet WHERE UserID = %s)"""
    cursor.execute(query, (userID,))
    fetch = cursor.fetchall()
    return {'data': fetch}


@app.route('/get_currency_transactions_in_date_range/<string:firstCurrencyCode>/<string:secondCurrencyCode>/<string'
           ':startDate>/<string:endDate>')
def get_currency_transactions_in_date_range(firstCurrencyCode, secondCurrencyCode, startDate, endDate):
    query = """SELECT TransactionID, Users.* FROM UserTransaction, Users
    WHERE MarketID IN (SELECT MarketID FROM Market WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s)
    AND TransactionDate BETWEEN %s AND %s
    AND UserTransaction.UserID = Users.UserID"""
    cursor.execute(query, (firstCurrencyCode, secondCurrencyCode, startDate, endDate))
    fetch1 = cursor.fetchall()
    cursor.execute(query, (secondCurrencyCode, firstCurrencyCode, startDate, endDate))
    fetch2 = cursor.fetchall()
    return {'data': fetch1 + fetch2}


@app.route('/get_transactions_summary_in_month/<string:month>/<string:year>')
def get_transactions_summary_in_month(month, year):
    query = """SELECT TargetCurrencyCode, SUM(BoughtAmount) AS TotalAmount, COUNT(*) AS TransactionCount
    FROM UserTransaction, Market
    WHERE MONTH(TransactionDate) = %s AND YEAR(TransactionDate) = %s AND UserTransaction.MarketID = Market.MarketID
    GROUP BY TargetCurrencyCode"""
    cursor.execute(query, (month, year))
    fetch = cursor.fetchall()
    return {'data': fetch}


@app.route('/get_top_5_users_with_most_exchanged_amount_in_market_in_year/<string:marketID>/<string:year>')
def get_top_5_users_with_most_exchanged_amount_in_market_in_year(marketID, year):
    query = """SELECT Users.*, SUM(BoughtAmount) AS TotalAmount
    FROM UserTransaction, Users
    WHERE MarketID = %s AND YEAR(TransactionDate) = %s AND UserTransaction.UserID = Users.UserID
    GROUP BY UserTransaction.UserID
    ORDER BY TotalAmount DESC
    LIMIT 5"""
    cursor.execute(query, (marketID, year))
    fetch = cursor.fetchall()
    return {'data': fetch}


@app.route(
    '/get_avg_count_currency_transaction_amount_in_date_range/<string:firstCurrencyCode>/<string:secondCurrencyCode>'
    '/<string:startDate>/<string:endDate>')
def get_avg_count_currency_transaction_amount_in_date_range(firstCurrencyCode, secondCurrencyCode, startDate, endDate):
    query = """SELECT AVG(BoughtAmount) AS AvgAmount, COUNT(*) AS TransactionCount
    FROM UserTransaction, Market
    WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s
    AND TransactionDate BETWEEN %s AND %s
    AND UserTransaction.MarketID = Market.MarketID"""
    cursor.execute(query, (firstCurrencyCode, secondCurrencyCode, startDate, endDate))
    fetch1 = cursor.fetchall()
    cursor.execute(query, (secondCurrencyCode, firstCurrencyCode, startDate, endDate))
    fetch2 = cursor.fetchall()
    return {firstCurrencyCode + '/' + secondCurrencyCode: fetch1, secondCurrencyCode + '/' + firstCurrencyCode: fetch2}


# endregion


if __name__ == '__main__':
    app.run(debug=True)
