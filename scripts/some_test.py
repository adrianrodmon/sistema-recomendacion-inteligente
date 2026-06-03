import requests

url = "https://image.tmdb.org/t/p/w500/rhIRbceoE9lR4veEXuwCC2wARtG.jpg"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=20
)

print(response.status_code)
print(response.headers.get("content-type"))
print(len(response.content))

import pandas as pd

df = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

print(df["poster_path"].sample(20).tolist())