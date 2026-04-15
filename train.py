import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

print("🚀 New training started...")

# Create artifacts folder
os.makedirs("artifacts", exist_ok=True)

# Load dataset
data = pd.read_csv("data/creditcard.csv")

# Drop unnecessary column
data = data.drop("Time", axis=1)

# Features and target
X = data.drop("Class", axis=1)
y = data["Class"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # 🔥 Probability

# Evaluation
print("📊 Accuracy:", accuracy_score(y_test, y_pred))

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("\n📊 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n📊 Sample Fraud Probabilities (first 10):")
print(y_proba[:10])

# Save model
with open("artifacts/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved successfully!")
