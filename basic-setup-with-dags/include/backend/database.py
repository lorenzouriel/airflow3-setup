import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import pyodbc

load_dotenv()

# Database configuration loaded from environment variables
DB_CONFIG = {
    'server': os.getenv('DB_SERVER'),
    'database': os.getenv('DB_NAME'),
    'username': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'driver': '{ODBC Driver 17 for SQL Server}'
}

def get_db_connection():
    """
    Establishes and returns a connection to the SQL Server database using the ODBC driver.

    Returns:
        pyodbc.Connection: A connection object to interact with the database.
    """
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']}"
    )
    return pyodbc.connect(conn_str)

def get_stocks():
    """
    Retrieves all stocks from the dbo.stocks table.

    Returns:
        list of pyodbc.Row: List containing stock records with fields (id, ticker, name, currency, created_at).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, ticker, name, currency, created_at FROM dbo.stocks;')
    stocks = cursor.fetchall()
    cursor.close()
    conn.close()
    return stocks

def fetch_yahoo_data(ticker, range_='1y', interval='1d'):
    """
    Fetches historical stock data from Yahoo Finance for a given ticker symbol.

    Args:
        ticker (str): The stock ticker symbol to query.
        range_ (str, optional): The time range for the data (default '1y' for one year).
        interval (str, optional): The data interval (default '1d' for daily).

    Returns:
        dict or None: Parsed JSON data from Yahoo Finance API if successful, otherwise None.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={range_}&interval={interval}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    return response.json()

def post_stock_data(stock_id, ticker, period):
    """
    Fetches historical stock data from Yahoo Finance and inserts it into the dbo.stock_data table.

    Args:
        stock_id (int): The database ID of the stock.
        ticker (str): The stock ticker symbol.
        period (str): The historical data period (e.g., '1y', '6mo', etc.).

    Behavior:
        - Fetches JSON data from Yahoo Finance.
        - Parses the timestamps and OHLCV (Open, High, Low, Close, Volume) data.
        - Inserts each daily data point into the stock_data table with the current timestamp.
        - Prints status messages to track progress.
    """
    print(f"Fetching data for ticker: {ticker}, period: {period}")
    json_data = fetch_yahoo_data(ticker, range_=period)

    if not json_data or "chart" not in json_data or "result" not in json_data["chart"]:
        print(f"No valid historical data found for ticker: {ticker}")
        return

    result = json_data["chart"]["result"][0]
    timestamps = result["timestamp"]
    indicators = result["indicators"]["quote"][0]

    conn = get_db_connection()
    cursor = conn.cursor()

    for i, ts in enumerate(timestamps):
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        open_price = indicators.get("open", [None])[i]
        close_price = indicators.get("close", [None])[i]
        high_price = indicators.get("high", [None])[i]
        low_price = indicators.get("low", [None])[i]
        volume = indicators.get("volume", [None])[i]

        query = """
            INSERT INTO dbo.stock_data (stock_id, [date], open_price, close_price, high_price, low_price, volume, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            stock_id, date, open_price, close_price,
            high_price, low_price, volume, datetime.now()
        )
        cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()