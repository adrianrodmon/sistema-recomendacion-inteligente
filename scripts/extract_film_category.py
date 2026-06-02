# scripts/02_extract_film_categories.py

import psycopg2
import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)

query = """
SELECT
    f.film_id,
    f.title,
    c.name AS category
FROM film f
JOIN film_category fc
    ON f.film_id = fc.film_id
JOIN category c
    ON fc.category_id = c.category_id
ORDER BY f.film_id
"""

df = pd.read_sql(query, conn)

print(df.head())

df.to_csv(
    "data/raw/film_categories.csv",
    index=False
)

conn.close()