import time
from backend.fetch_price import get_current_btc_price
from backend.data_manager import save_price

def track_bitcoin():
    while True:
        price = get_current_btc_price()
        if price is not None:
            save_price(price)
            time.sleep(10)

if __name__ == "__main__":
    print("Bitcoin tracker started...")
    track_bitcoin()
