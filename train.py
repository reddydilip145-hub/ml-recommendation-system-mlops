import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Create dummy dataset
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

models = {
    "RandomForest": RandomForestClassifier(n_estimators=100),
    "LogisticRegression": LogisticRegression()
}

mlflow.set_experiment("fraud-detection")

best_accuracy = 0
best_run_id = None

for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name) as run:

        model.fit(X_train, y_train)
        accuracy = model.score(X_test, y_test)

        # Log details
        mlflow.log_param("model_name", model_name)
        mlflow.log_metric("accuracy", accuracy)

        # Log model artifact
        mlflow.sklearn.log_model(model, artifact_path="model")

        print(f"{model_name} Accuracy: {accuracy}")

        # Track best model
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_run_id = run.info.run_id

# Register best model
model_uri = f"runs:/{best_run_id}/model"

registered_model = mlflow.register_model(
    model_uri=model_uri,
    name="BestFraudModel"
)

print(f"\nBest Model Accuracy: {best_accuracy}")
print(f"Registered Model Version: {registered_model.version}")

# 🔥 OPTIONAL: Move model to Production automatically
client = MlflowClient()

client.transition_model_version_stage(
    name="BestFraudModel",
    version=registered_model.version,
    stage="Production"
)

print("Model moved to Production!")