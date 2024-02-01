from flask import Flask, render_template, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection details
database_name = "project"
root_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database=database_name
)

cursor = root_db.cursor()

@app.route('/')
def index():
    # Fetch data from the database
    user_data = fetch_user_data_from_db()
    transaction_data = fetch_transaction_data_from_db()
    wallet_data = fetch_wallet_data_from_db()

    return render_template('test.html', userinfo=user_data, transactioninfo=transaction_data, walletinfo=wallet_data)

def fetch_user_data_from_db():
    query = "SELECT Username, Firstname, Lastname FROM Users WHERE UserID = %s"
    cursor.execute(query, (1,))  # Assuming UserID 1 for demo purposes
    user_data = cursor.fetchone()
    return user_data

def fetch_transaction_data_from_db():
    query = """SELECT PaidAmount, BoughtAmount, TransactionDate, MarketName
               FROM UserTransaction, Market 
               WHERE UserTransaction.UserID = %s AND UserTransaction.MarketID = Market.MarketID"""
    cursor.execute(query, (1,))  # Assuming UserID 1 for demo purposes
    transaction_data = cursor.fetchall()
    return transaction_data

def fetch_wallet_data_from_db():
    query = """SELECT CurrencyCode, Amount 
               FROM WalletCurrency
               WHERE WalletID IN (SELECT WalletID FROM Wallet WHERE UserID = %s)"""
    cursor.execute(query, (1,))  # Assuming UserID 1 for demo purposes
    wallet_data = cursor.fetchall()
    return wallet_data

if __name__ == '__main__':
    app.run(debug=True)
