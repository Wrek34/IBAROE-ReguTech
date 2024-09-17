import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import Adam

# Function to prepare time series data


def prepare_time_series(data, time_steps):
    X, y = [], []
    for i in range(len(data) - time_steps):
        X.append(data[i:(i + time_steps)])
        y.append(data[i + time_steps])
    return np.array(X), np.array(y)


# Generate sample data (replace this with real data in production)
dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
data = pd.Series(np.random.randn(len(dates)).cumsum(), index=dates)

# Prepare data for LSTM
time_steps = 30
X, y = prepare_time_series(data.values, time_steps)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(
    X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
X_test_scaled = scaler.transform(
    X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)

# Build the LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(time_steps, 1)),
    Dense(1)
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=50,
                    batch_size=32, validation_split=0.2, verbose=1)

# Evaluate the model
test_loss = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f'Test loss: {test_loss}')

# Function to make predictions


def predict_trend(model, scaler, last_30_days):
    scaled_data = scaler.transform(
        last_30_days.reshape(-1, 1)).reshape(1, time_steps, 1)
    prediction = model.predict(scaled_data)
    return prediction[0][0]


# Example usage
last_30_days = data.values[-30:].reshape(-1, 1)
trend_prediction = predict_trend(model, scaler, last_30_days)
print(f'Predicted trend for next day: {trend_prediction}')

# Save the model
model.save('ibaroe_trend_model.h5')
print("Model saved as 'ibaroe_trend_model.h5'")
