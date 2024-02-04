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
    Username char(30) NOT NULL PRIMARY KEY,
    UserPassword char(30) NOT NULL,
    FirstName char(30),
    LastName char(30),
    Address char(100),
    Email char(40))""")

cursor.execute("""CREATE TABLE IF NOT EXISTS Wallet(
    WalletID bigint NOT NULL PRIMARY KEY,
    Username char(30) NOT NULL,

    FOREIGN KEY(Username)
    REFERENCES Users(Username)
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
    Username char(30) NOT NULL,
    MarketID bigint NOT NULL,
    PaidAmount float NOT NULL,
    BoughtAmount float NOT NULL,
    TransactionDate datetime,
    
    FOREIGN KEY(Username)
    REFERENCES Users(Username)
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

# for username in range(1, 1000):
#     query = """UPDATE Users SET Username = %s WHERE UserID = %s"""
#     username = fake.user_name()
#
#     cursor.execute("""SELECT Username FROM Users WHERE Username = %s""", (username,))
#
#     if cursor.fetchall():
#         while cursor.fetchall():
#             username = fake.user_name()
#             cursor.execute("""SELECT Username FROM Users WHERE Username = %s""", (username,))
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


# region unused
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        data = request.json
        userid = data.get('userid')

        # Fetch user information
        user_query = "SELECT Username, FirstName, LastName FROM Users WHERE UserID = %s"
        cursor.execute(user_query, (userid,))
        user_info = cursor.fetchone()

        # Fetch user wallet balances
        wallet_query = """SELECT wc.CurrencyCode, wc.Amount
                          FROM WalletCurrency wc
                          INNER JOIN Wallet w ON wc.WalletID = w.WalletID
                          WHERE w.UserID = %s"""
        cursor.execute(wallet_query, (userid,))
        wallet_balances = cursor.fetchall()

        return jsonify(userinfo=user_info, wallet_balances=wallet_balances)
    else:
        # Handle the case when it's a regular GET request
        # Render the page with a placeholder user ID for demonstration purposes
        # You might want to adjust this based on your authentication logic
        return render_template('dashboard.html', userid='placeholder_user_id')


# @app.route('/trade')
# def trade():
#     return render_template('trade_window.html')


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


# endregion


# region user queries

@app.route('/get_user_profile/<string:username>')
def get_user_profile_data(username):
    query = """SELECT Username, Firstname, Lastname, Email, Address FROM Users WHERE Username = %s"""
    cursor.execute(query, (username,))
    fetch = cursor.fetchall()
    headings = ['Username', 'FirstName', 'LastName', 'Email', 'Address']
    return render_template('table.html', headings=headings, data=fetch)


@app.route('/get_user_wallet/<string:username>')
def get_user_wallet(username):
    query = """SELECT WalletID FROM Wallet WHERE Username = %s"""
    cursor.execute(query, (username,))
    walletId = cursor.fetchone()[0]
    query = """SELECT CurrencyCode, Amount FROM WalletCurrency WHERE WalletID = %s"""
    cursor.execute(query, (walletId,))
    fetch = cursor.fetchall()
    headings = ['CurrencyCode', 'Amount']
    return render_template('table.html', headings=headings, data=fetch)


@app.route('/get_user_transactions/<string:username>')
def get_user_transactions(username):
    query = """SELECT TransactionID, MarketName, PaidAmount, BoughtAmount, TransactionDate
    FROM UserTransaction, Market WHERE Username = %s AND UserTransaction.MarketID = Market.MarketID"""
    cursor.execute(query, (username,))
    fetch = cursor.fetchall()
    headings = ['TransactionID', 'MarketName', 'PaidAmount', 'BoughtAmount', 'TransactionDate']
    return render_template('table.html', headings=headings, data=fetch)


@app.route('/trade/<string:username>/<string:baseCurrency>/<string:targetCurrency>/<float:amount>')
def trade(username, baseCurrency, targetCurrency, amount):
    query = """SELECT Amount FROM WalletCurrency, Wallet
    WHERE WalletCurrency.WalletID = Wallet.WalletID AND Wallet.Username = %s AND CurrencyCode = %s"""
    cursor.execute(query, (username, baseCurrency))

    fetch = cursor.fetchone()
    if fetch is None:
        return "Trade Failed! Insufficient Balance"

    baseBalance = fetch[0]

    query = """SELECT ExchangeAmount FROM Market WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s"""
    cursor.execute(query, (baseCurrency, targetCurrency))
    exchangeAmount = cursor.fetchone()[0]

    if baseBalance >= amount * exchangeAmount:
        query = """UPDATE WalletCurrency, Wallet
        SET Amount = Amount - %s
        WHERE WalletCurrency.WalletID = Wallet.WalletID AND Wallet.Username = %s AND CurrencyCode = %s"""
        cursor.execute(query, (amount * exchangeAmount, username, baseCurrency))

        # If the target currency is not in the user's wallet, add it otherwise update the amount
        query = """INSERT INTO WalletCurrency (WalletID, CurrencyCode, Amount)
        VALUES ((SELECT WalletID FROM Wallet WHERE Username = %s), %s, %s)
        ON DUPLICATE KEY UPDATE Amount = Amount + %s"""
        cursor.execute(query, (username, targetCurrency, amount, amount))

        query = """INSERT INTO UserTransaction (Username, MarketID, PaidAmount, BoughtAmount, TransactionDate)
        VALUES (%s, (SELECT MarketID FROM Market WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s), %s, %s, %s)"""
        cursor.execute(query, (username, baseCurrency, targetCurrency, amount * exchangeAmount, amount, datetime.now()))

        root_db.commit()
        return "Trade Successful!"
    else:
        return "Trade Failed! Insufficient Balance"


# endregion


# region default queries
@app.route('/get_currency_transactions_in_date_range/<string:firstCurrencyCode>/<string:secondCurrencyCode>/<string'
           ':startDate>/<string:endDate>')
def get_currency_transactions_in_date_range(firstCurrencyCode, secondCurrencyCode, startDate, endDate):
    query = """SELECT UserTransaction.Username, FirstName, Lastname, TransactionID, MarketName,
     PaidAmount, BoughtAmount, TransactionDate
    FROM UserTransaction, Users, Market
    WHERE UserTransaction.MarketID IN (SELECT MarketID FROM Market
    WHERE (BaseCurrencyCode = %s AND TargetCurrencyCode = %s) OR (BaseCurrencyCode = %s AND TargetCurrencyCode = %s))
    AND TransactionDate BETWEEN %s AND %s
    AND UserTransaction.Username = Users.Username
    AND UserTransaction.MarketID = Market.MarketID
    ORDER BY TransactionDate DESC"""
    cursor.execute(query, (firstCurrencyCode, secondCurrencyCode, secondCurrencyCode, firstCurrencyCode,
                           startDate, endDate))
    fetch = cursor.fetchall()
    headings = ['Username', 'FirstName', 'LastName', 'TransactionID', 'MarketName',
                'PaidAmount', 'BoughtAmount', 'TransactionDate']
    return render_template('table.html', headings=headings, data=fetch)


@app.route('/get_transactions_summary_in_month/<string:month>/<string:year>')
def get_transactions_summary_in_month(month, year):
    query = """SELECT TargetCurrencyCode, SUM(BoughtAmount) AS TotalAmount, COUNT(*) AS TransactionCount
    FROM UserTransaction, Market
    WHERE MONTH(TransactionDate) = %s AND YEAR(TransactionDate) = %s AND UserTransaction.MarketID = Market.MarketID
    GROUP BY TargetCurrencyCode"""
    cursor.execute(query, (month, year))
    fetch = cursor.fetchall()

    headings = ['TargetCurrencyCode', 'TotalAmount', 'TransactionCount']
    return render_template('table.html', headings=headings, data=fetch)


@app.route('/get_top_5_users_with_most_exchanged_amount_in_market_in_year/<string:baseCurrencyCode>/'
           '<string:targetCurrencyCode>/<string:year>')
def get_top_5_users_with_most_exchanged_amount_in_market_in_year(baseCurrencyCode, targetCurrencyCode, year):
    query = """SELECT Users.Username, FirstName, LastName, SUM(BoughtAmount) AS TotalAmount
    FROM UserTransaction, Users
    WHERE UserTransaction.Username = Users.Username AND YEAR(TransactionDate) = %s AND MarketID IN 
    (SELECT MarketID FROM Market WHERE BaseCurrencyCode = %s AND TargetCurrencyCode = %s)
    GROUP BY UserTransaction.Username
    ORDER BY TotalAmount DESC
    LIMIT 5"""
    cursor.execute(query, (year, baseCurrencyCode, targetCurrencyCode))
    fetch = cursor.fetchall()

    headings = ['Username', 'FirstName', 'LastName', 'TotalAmount']
    return render_template('table.html', headings=headings, data=fetch)


@app.route(
    '/get_avg_count_currency_transaction_amount_in_date_range/<string:firstCurrencyCode>/<string:secondCurrencyCode>'
    '/<string:startDate>/<string:endDate>')
def get_avg_count_currency_transaction_amount_in_date_range(firstCurrencyCode, secondCurrencyCode, startDate, endDate):
    query = """SELECT AVG(BoughtAmount) AS AvgAmount, COUNT(*) AS TransactionCount
    FROM UserTransaction, Market
    WHERE ((BaseCurrencyCode = %s AND TargetCurrencyCode = %s) OR (BaseCurrencyCode = %s AND TargetCurrencyCode = %s))
    AND (TransactionDate BETWEEN %s AND %s)
    AND (UserTransaction.MarketID = Market.MarketID)"""
    cursor.execute(query, (firstCurrencyCode, secondCurrencyCode, secondCurrencyCode, firstCurrencyCode,
                           startDate, endDate))
    fetch = cursor.fetchall()

    headings = ['AvgAmount', 'TransactionCount']
    return render_template('table.html', headings=headings, data=fetch)


# endregion


if __name__ == '__main__':
    app.run(debug=True)
