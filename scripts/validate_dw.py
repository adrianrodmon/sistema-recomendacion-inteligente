# scripts/validate_dw.py

import psycopg2
import pandas as pd

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DB_CONFIG


def run_validation_queries(conn):

    validations = [
        {
            "name": "Cantidad de peliculas",
            "query": "SELECT COUNT(*) FROM film",
            "expected_min": 600,
            "expected_max": 1200
        },
        {
            "name": "Cantidad de clientes",
            "query": "SELECT COUNT(*) FROM customer",
            "expected_min": 500,
            "expected_max": 700
        },
        {
            "name": "Cantidad de alquileres",
            "query": "SELECT COUNT(*) FROM rental",
            "expected_min": 10000,
            "expected_max": 20000
        }
    ]

    print("=== VALIDACIONES ===\n")

    for val in validations:

        df = pd.read_sql(val["query"], conn)

        value = df.iloc[0, 0]

        status = (
            "OK"
            if val["expected_min"] <= value <= val["expected_max"]
            else "FALLO"
        )

        print(
            f"{val['name']}: {value} [{status}]"
        )


if __name__ == "__main__":

    conn = psycopg2.connect(**DB_CONFIG)

    run_validation_queries(conn)

    conn.close()