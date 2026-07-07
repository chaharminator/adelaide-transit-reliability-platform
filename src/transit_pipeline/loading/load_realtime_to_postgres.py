from pathlib import Path
import os

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
}


SILVER_REALTIME_DIR = Path("data/silver/gtfs_realtime")


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """
    return psycopg2.connect(**DB_CONFIG)


def load_vehicle_positions(connection) -> None:
    """
    Load silver-layer GTFS Realtime vehicle positions into PostgreSQL.
    """
    csv_file = SILVER_REALTIME_DIR / "vehicle_positions.csv"

    if not csv_file.exists():
        raise FileNotFoundError(f"Silver vehicle positions file not found: {csv_file}")

    df = pd.read_csv(csv_file)

    columns = [
        "entity_id",
        "trip_id",
        "route_id",
        "vehicle_id",
        "vehicle_label",
        "latitude",
        "longitude",
        "bearing",
        "speed",
        "vehicle_timestamp",
        "vehicle_datetime",
        "ingestion_file",
    ]

    df = df[columns]

    records = [tuple(row) for row in df.to_numpy()]

    insert_query = """
        INSERT INTO vehicle_positions (
            entity_id,
            trip_id,
            route_id,
            vehicle_id,
            vehicle_label,
            latitude,
            longitude,
            bearing,
            speed,
            vehicle_timestamp,
            vehicle_datetime,
            ingestion_file
        )
        VALUES %s
    """

    with connection.cursor() as cursor:
        execute_values(cursor, insert_query, records)

    print(f"Loaded {len(records)} rows into vehicle_positions")


def load_realtime_to_postgres() -> None:
    """
    Load GTFS Realtime silver tables into PostgreSQL.
    """
    print("Starting realtime load to PostgreSQL...")

    connection = get_connection()

    try:
        load_vehicle_positions(connection)
        connection.commit()
        print("Realtime data loaded into PostgreSQL successfully.")

    except Exception as error:
        connection.rollback()
        print("Realtime load failed. Transaction rolled back.")
        raise error

    finally:
        connection.close()
        print("Database connection closed.")


def main():
    load_realtime_to_postgres()


if __name__ == "__main__":
    main()