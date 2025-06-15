import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os

DATA_FILE = 'data/bitcoin_prices.csv'

def load_data():
    if not os.path.exists(DATA_FILE):
        print("Price data file not found")
        return None, None

    try:
        df = pd.read_csv(DATA_FILE)
    except pd.errors.EmptyDataError:
        print("Price data file is empty")
        return None, None

    if len(df) < 2:
        print("Not enough data to train.")
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

if __name__ == '__main__':
    X, y = load_data()

    if X is None or y is None:
        print("No data to train on.")
    else:
        model = train_model(X, y)
        predicted_price = predict_next_price(model, X)
        print(f"Predicted next BTC price: ${predicted_price:.2f}")
