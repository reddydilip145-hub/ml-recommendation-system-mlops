from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))

# 🔹 EXISTING API (example)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([list(data.values())])
    return jsonify({"prediction": int(prediction[0])})

# 🔥 ADD THIS HERE (health endpoint)
@app.route('/health')
def health():
    return {"status": "ok"}, 200

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
