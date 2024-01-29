import random
from flask import Flask, render_template
import mysql.connector
from faker import Faker
from datetime import datetime

root_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ُ12345678",
    database="ExchangeManagement"
)

cursor = root_db.cursor()

# region Initial Queries

cursor.execute("CREATE DATABASE IF NOT EXISTS ExchangeManagement")

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

# for walletID in range(1, 3000):
#     query = """INSERT INTO WalletCurrency (WalletID, CurrencyCode, Amount)
#      VALUES (%s, %s, %s)"""
#     currencyCode = fake.random_element(elements=('USD', 'EUR', 'GBP', 'JPY', 'IRR', 'CAD', 'AUD', 'CHF', 'RUB', 'CNY',
#                                                  'TRY', 'NZD', 'SEK', 'BRL', 'INR', 'ZAR'))
#     val = (walletID, currencyCode, fake.random_int(min=1, max=100000))
#     cursor.execute(query, val)
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


if __name__ == '__main__':
    app.run(debug=True)
