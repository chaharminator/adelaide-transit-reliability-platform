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

    df = df[columns].copy()

    # Convert source timestamps to nullable integers
    df["vehicle_timestamp"] = pd.to_numeric(
        df["vehicle_timestamp"],
        errors = "coerce"
    ).astype("Int64")

    # Reject records without a vehicle ID or timestamp
    invalid_rows = (
        df["vehicle_id"].isna() | (df["vehicle_id"].astype(str).str.strip() == "")
        | df["vehicle_timestamp"].isna()
    )

    invalid_count = int(invalid_rows.sum())

    if invalid_count > 0:
        raise ValueError(
            f"Found {invalid_count} vehicle records with missing IDs or timestamps."
        )

    # Convert missing pandas values to Python None
    df = df.astype(object).where(pd.notna(df), None)

    # Convert dataframe rows into tuples for PostgreSQL
    records = list(df.itertuples(index = False, name = None))

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
        ON CONFLICT (vehicle_id, vehicle_timestamp) DO NOTHING
    """

    with connection.cursor() as cursor:
        inserted_rows = execute_values(
            cursor,
            insert_query + "RETURNING position_id",
            records,
            fetch=True
        )

    print(f"Records received: {len(records)}")
    print(f"New records inserted: {len(inserted_rows)}") 
    print(f"Duplicate records skipped: {len(records) - len(inserted_rows)}")

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