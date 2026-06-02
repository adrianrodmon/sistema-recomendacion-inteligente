import requests
import time
import pandas as pd
import psycopg2


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    DB_CONFIG,
    TMDB_API_KEY,
    TMDB_BASE_URL,
    TMDB_IMAGE_BASE_URL
)

class TMDBClient:
    """
    Cliente para consumir TMDB API
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = TMDB_BASE_URL

        self.session = requests.Session()

        self.session.params = {
            "api_key": api_key,
            "language": "es-ES"
        }

        self.last_request_time = 0
        self.request_delay = 0.25

    def _rate_limit(self):
        current_time = time.time()

        elapsed = current_time - self.last_request_time

        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)

        self.last_request_time = time.time()

    def search_movie(self, title, year=None):

        self._rate_limit()

        url = f"{self.base_url}/search/movie"

        params = {
            "query": title
        }

        if year:
            params["year"] = int(year)

        response = self.session.get(url, params=params)

        if response.status_code == 200:
            return response.json()

        return None

    def get_movie_details(self, movie_id):

        self._rate_limit()

        url = f"{self.base_url}/movie/{movie_id}"

        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()

        return None

    def get_poster_url(self, poster_path, size="w500"):

        if not poster_path:
            return None

        return f"{TMDB_IMAGE_BASE_URL}{size}{poster_path}"


def search_film_in_tmdb(client, film_title, release_year=None):

    result = client.search_movie(film_title, release_year)

    if result and result.get("results"):
        return result["results"][0]

    return None


def get_all_films_from_db():

    conn = psycopg2.connect(**DB_CONFIG)

    query = """
    SELECT
        film_id,
        title,
        release_year
    FROM film
    ORDER BY film_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


if __name__ == "__main__":

    client = TMDBClient(TMDB_API_KEY)

    result = client.search_movie("The Matrix")

    print(result)