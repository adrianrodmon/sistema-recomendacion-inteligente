
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tmdb_api import TMDBClient
from config import TMDB_API_KEY

client = TMDBClient(TMDB_API_KEY)

movies = [
    "The Matrix",
    "Titanic",
    "Avatar",
    "Interstellar"
]

for movie in movies:

    result = client.search_movie(movie)

    print(f"\n{movie}")

    if result and result.get("results"):
        first = result["results"][0]

        print("Encontrada")
        print(first["title"])
        print(first.get("poster_path"))

    else:
        print("No encontrada")