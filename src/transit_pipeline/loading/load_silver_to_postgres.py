from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
}


SILVER_GTFS_DIR = Path("data/silver/gtfs_static")


def get_connection():
    """
    Create a connection to the PostgreSQL database.
    """
    return psycopg2.connect(**DB_CONFIG)


def load_csv_to_table(connection, csv_file: Path, table_name: str, columns: list[str]) -> None:
    """
    Load a CSV file into a PostgreSQL table.
    """
    df = pd.read_csv(csv_file)

    df = df[columns]

    records = [tuple(row) for row in df.to_numpy()]

    column_list = ", ".join(columns)
    insert_query = f"INSERT INTO {table_name} ({column_list}) VALUES %s"

    with connection.cursor() as cursor:
        execute_values(cursor, insert_query, records)

    print(f"Loaded {len(records)} rows into {table_name}")


def truncate_tables(connection) -> None:
    """
    Clear existing data from PostgreSQL tables before loading fresh data.
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            TRUNCATE TABLE stop_times, trips, stops, routes
            RESTART IDENTITY
            CASCADE;
        """)

    print("Existing warehouse tables truncated.")


def load_silver_to_postgres() -> None:
    """
    Load silver-layer GTFS CSV files into PostgreSQL warehouse tables.
    """
    print("Starting load from silver layer to PostgreSQL...")

    connection = get_connection()

    try:
        truncate_tables(connection)

        load_csv_to_table(
            connection=connection,
            csv_file=SILVER_GTFS_DIR / "routes.csv",
            table_name="routes",
            columns=[
                "route_id",
                "agency_id",
                "route_short_name",
                "route_long_name",
                "route_type",
            ],
        )

        load_csv_to_table(
            connection=connection,
            csv_file=SILVER_GTFS_DIR / "stops.csv",
            table_name="stops",
            columns=[
                "stop_id",
                "stop_name",
                "stop_lat",
                "stop_lon",
            ],
        )

        load_csv_to_table(
            connection=connection,
            csv_file=SILVER_GTFS_DIR / "trips.csv",
            table_name="trips",
            columns=[
                "trip_id",
                "route_id",
                "service_id",
                "trip_headsign",
                "direction_id",
                "shape_id",
            ],
        )

        load_csv_to_table(
            connection=connection,
            csv_file=SILVER_GTFS_DIR / "stop_times.csv",
            table_name="stop_times",
            columns=[
                "trip_id",
                "arrival_time",
                "departure_time",
                "stop_id",
                "stop_sequence",
            ],
        )

        connection.commit()
        print("Silver layer loaded into PostgreSQL successfully.")

    except Exception as error:
        connection.rollback()
        print("Load failed. Transaction rolled back.")
        raise error

    finally:
        connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    load_silver_to_postgres()