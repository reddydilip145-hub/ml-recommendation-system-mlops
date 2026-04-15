import kagglehub
import shutil
import os

# Download dataset
path = kagglehub.dataset_download("arockiaselciaa/creditcardcsv")

print("Downloaded to:", path)

# Create data folder
os.makedirs("data", exist_ok=True)

# Copy CSV to your project folder
for file in os.listdir(path):
    if file.endswith(".csv"):
        src = os.path.join(path, file)
        dst = os.path.join("data", "creditcard.csv")
        shutil.copy(src, dst)
        print("Dataset copied to:", dst)