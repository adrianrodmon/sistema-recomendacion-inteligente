import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "dvdrental",
    "user": "postgres",
    "password": "admin1234",
    "port": "5432"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)