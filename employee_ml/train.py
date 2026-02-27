import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression

fake_hosts = ["blogspot", "wordpress", "weebly", ".tk", ".ml", ".xyz"]

def extract_features(url):
    url = url.lower()
    return [
        len(url),
        1 if "careers" in url or "jobs" in url else 0,
        1 if any(x in url for x in fake_hosts) else 0,
        1 if url.startswith("https") else 0
    ]

# load dataset
df = pd.read_csv("dataset.csv")

X = df["url"].apply(extract_features).tolist()
y = df["label"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model retrained successfully")