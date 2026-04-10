import pickle

with open("artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

data = [[30, 50000]]

prediction = model.predict(data)

print("Prediction:", prediction)
