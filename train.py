import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample dataset
data = {
    "age": [22, 25, 47, 52, 46, 56],
    "salary": [15000, 29000, 48000, 60000, 52000, 65000],
    "purchased": [0, 0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["age", "salary"]]
y = df["purchased"]

model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully")
