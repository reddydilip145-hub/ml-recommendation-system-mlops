from flask import Flask, request, jsonify
import pickle
import numpy as np

print("🔥 NEW APP VERSION RUNNING 🔥")

app = Flask(__name__)

# Load model safely
try:
    with open("artifacts/model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print("❌ Error loading model:", e)
    model = None


@app.route("/")
def home():
    return "Fraud Detection API Running 🚀"


# ✅ Health check (for Kubernetes probes)
@app.route("/health")
def health():
    if model is not None:
        return jsonify({"status": "OK"}), 200
    else:
        return jsonify({"status": "Model not loaded"}), 500


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()
        print("Incoming data:", data)

        # Validate input
        if not data or "features" not in data:
            return jsonify({"error": "Invalid input. Required field: features"}), 400

        features = data["features"]

        if not isinstance(features, list):
            return jsonify({"error": "Features must be a list"}), 400

        if len(features) != 29:
            return jsonify({"error": "Exactly 29 features required"}), 400

        # Convert to numpy
        input_data = np.array(features).reshape(1, -1)

        # Prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]  # 🔥 probability

        result = "Fraud" if prediction == 1 else "Not Fraud"

        return jsonify({
            "prediction": result,
            "fraud_probability": float(probability)
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
