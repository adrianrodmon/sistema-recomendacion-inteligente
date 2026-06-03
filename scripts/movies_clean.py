import pandas as pd

df = pd.read_csv(
    "data/raw/movies_metadata.csv",
    low_memory=False
)

df = df[
    [
        "id",
        "title",
        "overview",
        "poster_path",
        "genres",
        "vote_average",
        "popularity"
    ]
]

df = df.dropna(
    subset=[
        "title",
        "overview",
        "poster_path"
    ]
)

df = df.drop_duplicates(
    subset=["title"]
)

print(df.shape)

df.to_csv(
    "data/processed/movies_clean.csv",
    index=False
)