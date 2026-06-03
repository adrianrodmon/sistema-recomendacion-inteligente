import psycopg2
import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)

query = """
SELECT
    film_id,
    title,
    description,
    release_year,
    rental_rate,
    rating
FROM film
ORDER BY film_id
"""

df = pd.read_sql(query, conn)

print(df.head())

df.to_csv(
    "data/raw/films.csv",
    index=False,
    encoding="utf-8"
)

conn.close()

print(f"Películas exportadas: {len(df)}")