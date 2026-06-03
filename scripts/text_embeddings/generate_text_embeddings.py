import os
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer

os.makedirs(
    "data/embeddings",
    exist_ok=True
)

df = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

df = df.fillna("")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

texts = df["overview"].tolist()

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

np.save(
    "data/embeddings/text_embeddings.npy",
    embeddings
)

np.save(
    "data/embeddings/text_movie_ids.npy",
    df["id"].values
)

print(
    f"Embeddings generados: {embeddings.shape}"
)