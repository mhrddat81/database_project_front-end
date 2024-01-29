import random
from flask import Flask, render_template, request, jsonify
import mysql.connector
from faker import Faker
from datetime import datetime

root_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="project"
)

cursor = root_db.cursor()

# region Initial Queries

cursor.execute("CREATE DATABASE IF NOT EXISTS project")

# region Tables Creation

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
    UserID bigint NOT NULL PRIMARY KEY,
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

hardcoded_username = 'admin'
hardcoded_password = 'admin'

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/trade_window')
def trade_window():
    return render_template('trade_window.html')


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

    if entered_username == hardcoded_username and entered_password == hardcoded_password:
        return jsonify(success=True)
    else:
        return jsonify(success=False)

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


@app.route('/get_avg_count_currency_transaction_amount_in_date_range/<string:firstCurrencyCode>/<string:secondCurrencyCode>'
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
