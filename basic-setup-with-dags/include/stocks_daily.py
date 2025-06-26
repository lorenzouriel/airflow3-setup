import os
from datetime import datetime
from dotenv import load_dotenv
from backend.database import get_stocks, post_stock_data

load_dotenv()

def load_stock_daily():
    """
    Fetches daily stock data for all the stocks in the database and inserts it into the dbo.stock_data table.
    """
    stocks = get_stocks()

    for stock in stocks:
        stock_id, ticker, name, currency, created_at = stock
        print(f"Loading daily data for {ticker} ({name})...")
        post_stock_data(stock_id, ticker, period="1d")
    
    print("Daily stock data loaded successfully.")

if __name__ == "__main__":
    load_stock_daily()