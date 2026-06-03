import os
import requests
import pandas as pd

from tqdm import tqdm

POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

OUTPUT_DIR = "data/posters"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

df = pd.read_csv(
    "data/processed/movies_sample_1000.csv"
)

downloaded = 0

for _, row in tqdm(
    df.iterrows(),
    total=len(df)
):

    movie_id = row["id"]
    poster_path = row["poster_path"]

    if pd.isna(poster_path):
        continue

    url = POSTER_BASE_URL + poster_path

    filename = f"{movie_id}.jpg"

    save_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    if os.path.exists(save_path):
        downloaded += 1
        continue

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code == 200:

            with open(
                save_path,
                "wb"
            ) as f:

                f.write(response.content)

            downloaded += 1

    except Exception:
        pass

print(f"\nPosters descargados: {downloaded}")