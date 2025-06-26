import os
from dotenv import load_dotenv
import yfinance as yf
from datetime import datetime
import pyodbc

load_dotenv()

DB_CONFIG = {
    'server': os.getenv('DB_SERVER') or 'localhost',
    'database': os.getenv('DB_NAME'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'driver': '{ODBC Driver 17 for SQL Server}'
}

def get_db_connection():
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']}"
    )
    return pyodbc.connect(conn_str)

def get_stocks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, ticker, name, currency, created_at FROM investment.stocks;')
        stocks = cursor.fetchall()
        cursor.close()
        conn.close()
        return stocks
    except pyodbc.Error as e:
        print(f"Error connecting or querying the database: {e}")
        return []

def post_stock_data(stock_id, ticker, period):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print(f"Fetching data for ticker: {ticker}, period: {period}")
        ticker_data = yf.Ticker(ticker)
        historical_data = ticker_data.history(period=period)

        if historical_data.empty:
            print(f"No historical data found for ticker: {ticker}")
            return

        for date, row in historical_data.iterrows():
            query = """
                INSERT INTO investment.stock_data (stock_id, [date], open_price, close_price, high_price, low_price, volume, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (
                stock_id, date.strftime('%Y-%m-%d'), row['Open'], row['Close'],
                row['High'], row['Low'], row['Volume'], datetime.now()
            )
            cursor.execute(query, values)
            print(f"Data inserted for {ticker} on {date.strftime('%Y-%m-%d')}")

        conn.commit()
        print(f"Data insertion completed for ticker: {ticker}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")