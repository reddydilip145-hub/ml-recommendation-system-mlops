from flask import Flask, request, jsonify
import pickle
import numpy as np

print("🔥 NEW APP VERSION RUNNING 🔥")

app = Flask(__name__)

# Load model
with open("artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "Fraud Detection API Running 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("Incoming data:", data)

        # Validate input
        if not data or "features" not in data:
            return jsonify({"error": "Invalid input. Required field: features"}), 400

        features = data["features"]

        # Validate length
        if len(features) != 29:
           return jsonify({"error": "Exactly 29 features required"}), 400

        input_data = np.array(features).reshape(1, -1)

        prediction = model.predict(input_data)[0]

        result = "Fraud" if prediction == 1 else "Not Fraud"

        return jsonify({"prediction": result})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)	