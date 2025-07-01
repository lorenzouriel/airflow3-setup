from datetime import datetime, timedelta
from dotenv import load_dotenv
from .backend.database import get_stocks, post_stock_data
import time

load_dotenv()

def load_stock_historical():
    """
    Fetches historical stock data for all the stocks in the database and inserts it into the dbo.stock_data table.
    Only loads historical data if created_at is within the last 24 hours.
    """
    stocks = get_stocks()

    for stock in stocks:
        stock_id, ticker, name, currency, created_at = stock

        if datetime.now() - created_at <= timedelta(days=1):
            post_stock_data(stock_id, ticker, period="1y")
            time.sleep(5)
        else:
            print(f"[INFO] Skipping {ticker} ({name}): created_at is older than 24 hours.")

    print("[DONE] Historical stock data loading completed.")

if __name__ == "__main__":
    load_stock_historical()