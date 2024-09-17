from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the trained model
model = load_model('ibaroe_trend_model.h5')

# Initialize scaler (you'd need to save and load the scaler in a real application)
scaler = StandardScaler()


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'last_30_days' not in data:
        return jsonify({'error': 'Missing last_30_days data'}), 400

    last_30_days = np.array(data['last_30_days']).reshape(-1, 1)

    # In a real application, you'd load the saved scaler
    scaler.fit(last_30_days)

    scaled_data = scaler.transform(last_30_days).reshape(1, 30, 1)
    prediction = model.predict(scaled_data)

    return jsonify({'prediction': float(prediction[0][0])})


if __name__ == '__main__':
    app.run(debug=True)
