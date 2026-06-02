import os
import time
import requests
import pandas as pd
import psycopg2

from tqdm import tqdm

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    DB_CONFIG,
    POSTERS_PATH,
    TMDB_API_KEY
)

from tmdb_api import (
    TMDBClient,
    search_film_in_tmdb
)


def download_image(url, save_path):

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        with open(save_path, "wb") as file:
            file.write(response.content)

        return True

    except Exception as e:

        print(f"Error descargando {url}")
        print(e)

        return False


def get_poster_filename(film_id, title):

    safe_title = (
        title
        .replace(" ", "_")
        .replace("/", "_")
    )

    return f"{film_id:04d}_{safe_title}.jpg"


def download_posters_for_all_films(conn, limit=None):

    query = """
    SELECT
        film_id,
        title,
        release_year
    FROM film
    ORDER BY film_id
    """

    films = pd.read_sql(query, conn)

    if limit:
        films = films.head(limit)

    print(f"Procesando {len(films)} peliculas")

    client = TMDBClient(TMDB_API_KEY)

    results = []

    for _, row in tqdm(
        films.iterrows(),
        total=len(films)
    ):

        film_id = row["film_id"]
        title = row["title"]
        year = row["release_year"]

        result = {
            "film_id": film_id,
            "title": title,
            "poster_downloaded": False,
            "tmdb_id": None,
            "poster_path": None
        }

        tmdb_movie = search_film_in_tmdb(
            client,
            title,
            year
        )

        if tmdb_movie:

            poster_path = tmdb_movie.get(
                "poster_path"
            )

            if poster_path:

                poster_url = client.get_poster_url(
                    poster_path
                )

                filename = get_poster_filename(
                    film_id,
                    title
                )

                save_path = os.path.join(
                    POSTERS_PATH,
                    filename
                )

                if download_image(
                    poster_url,
                    save_path
                ):

                    result["poster_downloaded"] = True
                    result["tmdb_id"] = tmdb_movie.get("id")
                    result["poster_path"] = poster_path

        results.append(result)

        time.sleep(0.1)

    results_df = pd.DataFrame(results)

    log_path = os.path.join(
        POSTERS_PATH,
        "poster_download_log.csv"
    )

    results_df.to_csv(
        log_path,
        index=False
    )

    downloaded = sum(
        1
        for r in results
        if r["poster_downloaded"]
    )

    print(
        f"\nResumen: {downloaded}/{len(results)} posters descargados"
    )

    return results_df


def verify_downloaded_posters():

    files = os.listdir(POSTERS_PATH)

    jpg_files = [
        f
        for f in files
        if f.endswith(".jpg")
    ]

    print(
        f"Archivos JPG encontrados: {len(jpg_files)}"
    )

    return len(jpg_files)


if __name__ == "__main__":

    conn = psycopg2.connect(**DB_CONFIG)

    print("=== DESCARGA DE POSTERS ===")

    download_posters_for_all_films(
        conn,
        limit=10
    )

    verify_downloaded_posters()

    conn.close()

    print("=== FIN ===")