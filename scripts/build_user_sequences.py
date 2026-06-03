import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from db_connection import get_connection

conn = get_connection()

query = """
SELECT
    r.customer_id,
    r.rental_date,
    c.name AS genre
FROM rental r
JOIN inventory i
    ON r.inventory_id = i.inventory_id
JOIN film f
    ON i.film_id = f.film_id
JOIN film_category fc
    ON f.film_id = fc.film_id
JOIN category c
    ON fc.category_id = c.category_id
ORDER BY
    customer_id,
    rental_date
"""

df = pd.read_sql(query, conn)

conn.close()

print(df.head())

print(df.shape)

df.to_csv(
    "data/processed/user_genre_sequences.csv",
    index=False
)

import pandas as pd

df = pd.read_csv(
    "data/processed/user_genre_sequences.csv"
)

user_sequences = (
    df.groupby("customer_id")["genre"]
      .apply(list)
      .reset_index()
)

print(user_sequences.head())

print(df.shape)

print(df["customer_id"].nunique())

print(df["genre"].nunique())