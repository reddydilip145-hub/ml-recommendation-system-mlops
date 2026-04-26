from flask import Flask, request, jsonify
import mlflow.pyfunc
import numpy as np

app = Flask(__name__)

# 🔥 Load model from MLflow (Production)
model = mlflow.pyfunc.load_model("models:/BestFraudModel/Production")

# 🔹 Home route
@app.route("/")
def home():
    return "MLflow Model API is running!"

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

# 🔥 Run app on different port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)