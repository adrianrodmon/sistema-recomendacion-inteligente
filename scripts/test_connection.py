# test_connection.py

import psycopg2
import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG

conn = psycopg2.connect(**DB_CONFIG)

query = """
SELECT film_id, title, release_year
FROM film
LIMIT 10
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()