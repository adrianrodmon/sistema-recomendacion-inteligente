import pandas as pd

df = pd.read_csv(
    "data/raw/movies_metadata.csv",
    low_memory=False
)

print(df.shape)

print(df.columns)

print(df[[
    "title",
    "overview",
    "poster_path"
]].head())