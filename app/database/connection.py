import os
import mysql.connector
from typing import Generator

# Read connection parameters from environment variables (defaults to local settings)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Babajani110"),
    "database": os.getenv("DB_NAME", "fastapiappdb")
}

def get_db_cursor() -> Generator:
    """FastAPI dependency that yields a database cursor and ensures cleanup."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)  # Returns rows as Python dictionaries
    try:
        yield cursor
        conn.commit()  # Automatically commits transactions on successful routes
    except Exception:
        conn.rollback()  # Rolls back changes if an error occurs during execution
        raise
    finally:
        cursor.close()
        conn.close()  # Guarantees database connections are closed after the request finishes

if __name__ == "__main__":
    print(f"Testing MySQL connection to host: {DB_CONFIG['host']} | db: {DB_CONFIG['database']}...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Success! Database connection established.")
        conn.close()
    except mysql.connector.Error as e:
        print("Connection Failed:", e)