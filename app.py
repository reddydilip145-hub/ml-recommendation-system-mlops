from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
try:
    with open("artifacts/model.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    print("Error loading model:", e)
    model = None

@app.route('/')
def home():
    return "Fraud Detection Model Running 🚀"

@app.route('/health')
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500

        data = request.get_json()

        # Validate input
        if not data or 'age' not in data or 'salary' not in data:
            return jsonify({
                "error": "Invalid input. Required fields: age, salary"
            }), 400

        age = data['age']
        salary = data['salary']

        features = [[age, salary]]

        prediction = model.predict(features)

        return jsonify({
            "input": {"age": age, "salary": salary},
            "prediction": int(prediction[0])
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
