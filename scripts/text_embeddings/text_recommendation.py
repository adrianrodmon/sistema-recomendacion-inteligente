import numpy as np
import pandas as pd

movies = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

similarity_matrix = np.load(
    "data/embeddings/text_similarity.npy"
)


def recommend_by_title(
    title,
    top_k=5
):

    matches = movies[
        movies["title"]
        .str.lower()
        ==
        title.lower()
    ]

    if len(matches) == 0:

        print(
            "Película no encontrada"
        )
        return

    idx = matches.index[0]

    similarities = similarity_matrix[idx]

    indices = (
        similarities.argsort()[::-1]
    )

    print(
        f"\nRecomendaciones para: {title}\n"
    )

    count = 0

    for i in indices:

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