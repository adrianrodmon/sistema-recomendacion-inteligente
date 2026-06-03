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
        "genres",
        "poster_path",
        "popularity",
        "vote_average",
        "release_date"
    ]
]

df = df.dropna(
    subset=[
        "title",
        "overview",
        "poster_path"
    ]
)

df.to_csv(
    "data/processed/movies_clean.csv",
    index=False
)

print(df.shape)