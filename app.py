from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

app = Flask(__name__)

# 🔥 Load model using pickle (from artifacts folder)
model_path = os.path.join(os.path.dirname(__file__), "artifacts", "model.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# 🔹 Home route
@app.route("/")
def home():
    return "Fraud Detection API is running!"

# 🔹 Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json["input"]
        prediction = model.predict(np.array(data))
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

# 🔹 Health check
@app.route('/health')
def health():
    return {"status": "ok"}, 200

# 🔥 IMPORTANT: use port 5000 (matches Kubernetes service)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)