import numpy as np
import pandas as pd

movie_ids = np.load(
    "data/embeddings/movie_ids.npy"
)

movies = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

available = movies[
    movies["id"].isin(movie_ids)
]

print(
    available[
        ["title"]
    ].head(20)
)