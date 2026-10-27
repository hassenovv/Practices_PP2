"""Opens a connection to PostgreSQL using settings from config.py."""
import psycopg2
from config import load_config


def get_connection():
    config = load_config()
    return psycopg2.connect(**config)


if __name__ == "__main__":
    try:
        with get_connection() as conn:
            print("Connected to PostgreSQL server.")
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                print(cur.fetchone()[0])
    except (psycopg2.DatabaseError, Exception) as error:
        print("Connection failed:", error)
