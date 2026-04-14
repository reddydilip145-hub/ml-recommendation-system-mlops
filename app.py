from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
with open("artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "Fraud Detection Model Running 🚀"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [[data['age'], data['salary']]]
    prediction = model.predict(features)
    return jsonify({"prediction": int(prediction[0])})

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
