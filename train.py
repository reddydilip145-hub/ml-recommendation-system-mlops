import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import os

# Create artifacts folder
os.makedirs("artifacts", exist_ok=True)

# Sample dataset
data = {
    "age": [25, 35, 45, 50],
    "salary": [20000, 40000, 60000, 80000],
    "purchased": [0, 0, 1, 1]
}

df = pd.DataFrame(data)

X = df[["age", "salary"]]
y = df["purchased"]

model = LogisticRegression()
model.fit(X, y)

with open("artifacts/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved")
