# File: backend/fetch_price.py
import requests

def get_current_btc_price():
    try:
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
        response = requests.get(url)
        data = response.json()
        price = data['bitcoin']['usd']
        return price

    except Exception as e:
        print("Error fetching price:", e)
        return None



if __name__ == "__main__":
    price = get_current_btc_price()
    print("Current BTC Price: $", price)
