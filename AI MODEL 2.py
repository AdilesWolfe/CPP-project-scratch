import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from pandas_datareader import data

# Load historical stock data (e.g., from Yahoo Finance)
start_date = '2010-01-01'
end_date = '2023-04-10'
stock_symbol = 'AAPL'  # Example: Apple Inc.
stock_data = data.DataReader(stock_symbol, 'yahoo', start_date, end_date)

# Extract closing prices
closing_prices = stock_data['Close'].values.reshape(-1, 1)

# Normalize data
scaler = MinMaxScaler()
scaled_prices = scaler.fit_transform(closing_prices)

# Create sequences for LSTM input
sequence_length = 30  # Number of past days to consider
X, y = [], []
for i in range(len(scaled_prices) - sequence_length):
    X.append(scaled_prices[i:i + sequence_length])
    y.append(scaled_prices[i + sequence_length])

X, y = np.array(X), np.array(y)

# Split data into train and test sets
train_size = int(0.8 * len(X))
X_train, y_train = X[:train_size], y[:train_size]
X_test, y_test = X[train_size:], y[train_size:]

# Build the LSTM model
model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(64, input_shape=(sequence_length, 1)))
model.add(tf.keras.layers.Dense(1))  # Output layer

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Make predictions
predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

# Visualize actual vs. predicted prices
plt.figure(figsize=(12, 6))
plt.plot(stock_data.index[train_size + sequence_length:], y_test, label='Actual Prices')
plt.plot(stock_data.index[train_size + sequence_length:], predicted_prices, label='Predicted Prices')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title(f'{stock_symbol} Stock Price Prediction')
plt.legend()
plt.show()
