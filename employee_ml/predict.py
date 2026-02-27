import pandas as pd

# load trusted dataset
df = pd.read_csv("dataset.csv")

trusted_urls = df[df["label"]=="real"]["url"].str.lower().tolist()

url = input("Enter company careers URL: ").lower()

if any(trusted in url for trusted in trusted_urls):
    print("Result: REAL company")
else:
    print("Result: FAKE company")