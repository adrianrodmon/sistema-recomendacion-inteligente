import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "dvdrental"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}

TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/"

DATA_RAW_PATH = "data/raw/"
DATA_PROCESSED_PATH = "data/processed/"
POSTERS_PATH = "data/posters/"

os.makedirs(DATA_RAW_PATH, exist_ok=True)
os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)
os.makedirs(POSTERS_PATH, exist_ok=True)