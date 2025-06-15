import streamlit as st
import pandas as pd
import numpy as np
import os
import time
import requests
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


DATA_FILE = 'data/bitcoin_prices.csv'
st.set_page_config(page_title="Bitcoin Price Tracker", layout="centered")


def fetch_current_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
    try:
        response = requests.get(url)
        data = response.json()
        return data['bitcoin']['usd']
    except:
        return None


def save_price(price):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    new_data = {'Time': timestamp, 'Price': price}

    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])

    df.to_csv(DATA_FILE, index=False)
    st.success(f"{timestamp} | Price saved: ${price}")


def load_data():
    if not os.path.exists(DATA_FILE):
        return None, None
    df = pd.read_csv(DATA_FILE)
    if df.empty:
        return None, None

    X = np.array(range(len(df))).reshape(-1, 1)
    y = df['Price'].values.reshape(-1, 1)
    return X, y


def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model


def predict_next_price(model, X):
    next_time_step = [[len(X)]]
    predicted_price = model.predict(next_time_step)
    return predicted_price[0][0]


st.title(" Bitcoin Price Tracker & Predictor")


if st.button(" Fetch Current Price"):
    price = fetch_current_price()
    if price:
        save_price(price)
    else:
        st.error("Failed to fetch real-time data.")

if st.button(" Predict Next Price"):
    X, y = load_data()
    if X is None or y is None:
        st.warning("Not enough data. Please fetch prices first.")
    else:
        model = train_model(X, y)
        predicted = predict_next_price(model, X)
        st.success(f" Predicted Next BTC Price: ${predicted:.2f}")


if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    if not df.empty:
        df['Time'] = pd.to_datetime(df['Time'])

        st.subheader(" Price History")
        fig, ax = plt.subplots()
        ax.plot(df['Time'], df['Price'], marker='o', color='orange', label='Real Prices')
        ax.set_xlabel("Time")
        ax.set_ylabel("Price (USD)")
        ax.set_title("Bitcoin Price Over Time")
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
