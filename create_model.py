from sklearn.linear_model import LogisticRegression
import pickle

# Create dummy model
model = LogisticRegression()

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("model.pkl created successfully")