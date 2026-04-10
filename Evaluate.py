import pandas as pd
import pickle
from sklearn.metrics import accuracy_score

data = {
    "age": [30, 40, 50],
    "salary": [30000, 50000, 70000],
    "purchased": [0, 1, 1]
}

df = pd.DataFrame(data)

X_test = df[["age", "salary"]]
y_test = df["purchased"]

with open("artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy}")
