import pandas as pd
import pickle
from sklearn.metrics import accuracy_score

# Sample test data
data = {
    "age": [30, 40, 50],
    "salary": [30000, 50000, 70000],
    "purchased": [0, 1, 1]
}

df = pd.DataFrame(data)

X_test = df[["age", "salary"]]
y_test = df["purchased"]

model = pickle.load(open("model.pkl", "rb"))

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(accuracy)
