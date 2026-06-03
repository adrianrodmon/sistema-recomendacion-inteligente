import numpy as np
import pandas as pd

movie_ids = np.load(
    "data/embeddings/movie_ids.npy"
)

similarity_matrix = np.load(
    "data/embeddings/visual_similarity.npy"
)

movies = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

movies = movies[
    movies["id"].isin(movie_ids)
].reset_index(drop=True)


def recommend_by_title(
    title,
    top_k=5
):

    matches = movies[
        movies["title"].str.lower()
        ==
        title.lower()
    ]

    if len(matches) == 0:

        print("Película no encontrada")
        return

    idx = matches.index[0]

    similarities = similarity_matrix[idx]

    recommended_idx = (
        similarities.argsort()[::-1]
    )

    print(
        f"\nRecomendaciones para: {title}\n"
    )

    count = 0

    for i in recommended_idx:

        if i == idx:
            continue

        print(
            f"{movies.iloc[i]['title']} "
            f"({similarities[i]:.4f})"
        )

        count += 1

        if count >= top_k:
            break


recommend_by_title(
    "Cell 213"
)