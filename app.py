from flask import Flask, request, jsonify
import pickle
import numpy as np

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

        # Expecting 30 features
        features = data["features"]

        # Convert to numpy array
        input_data = np.array(features).reshape(1, -1)

        prediction = model.predict(input_data)[0]

        result = "Fraud" if prediction == 1 else "Not Fraud"

        return jsonify({
            "prediction": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
