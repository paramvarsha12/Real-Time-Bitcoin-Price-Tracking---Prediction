import pandas as pd
import os
import time

DATA_FILE = 'data/bitcoin_prices.csv'

def save_price(price):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S') 
    new_data = {'Time': timestamp, 'Price': price}

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])

    df.to_csv(DATA_FILE, index=False)
    print(f"{timestamp} | Price saved: ${price}")
