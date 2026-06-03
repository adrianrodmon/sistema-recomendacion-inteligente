# scripts/03_extract_rentals.py

import psycopg2
import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)

query = """
SELECT
    r.rental_id,
    r.rental_date,
    c.customer_id,
    f.film_id,
    f.title
FROM rental r
JOIN inventory i
    ON r.inventory_id = i.inventory_id
JOIN film f
    ON i.film_id = f.film_id
JOIN customer c
    ON r.customer_id = c.customer_id
ORDER BY customer_id, rental_date
"""

df = pd.read_sql(query, conn)

print(df.head())

df.to_csv(
    "data/raw/rentals.csv",
    index=False
)

conn.close()