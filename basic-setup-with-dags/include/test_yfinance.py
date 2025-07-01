import requests

def test_yfinance():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1y&interval=1d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)
    print("Response:", response.text[:300]) 