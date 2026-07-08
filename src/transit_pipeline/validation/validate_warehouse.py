import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
}


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """
    return psycopg2.connect(**DB_CONFIG)


def run_count_check(cursor, table_name: str) -> bool:
    """
    Check whether a table contains at least one row.
    """
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    row_count = cursor.fetchone()[0]

    if row_count > 0:
        print(f"PASS: {table_name} has {row_count} rows.")
        return True

    print(f"FAIL: {table_name} is empty.")
    return False


def run_zero_result_check(cursor, check_name: str, query: str) -> bool:
    """
    Run a validation query where the expected result should be zero.
    """
    cursor.execute(query)
    issue_count = cursor.fetchone()[0]

    if issue_count == 0:
        print(f"PASS: {check_name}")
        return True

    print(f"FAIL: {check_name} found {issue_count} issue(s).")
    return False


def validate_warehouse() -> None:
    """
    Run warehouse validation checks for static and realtime GTFS data.
    """
    print("Starting warehouse validation checks...")

    checks_passed = 0
    checks_failed = 0

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            tables_to_check = [
                "routes",
                "stops",
                "trips",
                "stop_times",
                "vehicle_positions",
            ]

            for table_name in tables_to_check:
                passed = run_count_check(cursor, table_name)

                if passed:
                    checks_passed += 1
                else:
                    checks_failed += 1

            validation_checks = [
                (
                    "vehicle_positions latitude/longitude should not be null",
                    """
                    SELECT COUNT(*)
                    FROM vehicle_positions
                    WHERE latitude IS NULL
                       OR longitude IS NULL;
                    """,
                ),
                (
                    "vehicle_positions latitude should be between -90 and 90",
                    """
                    SELECT COUNT(*)
                    FROM vehicle_positions
                    WHERE latitude < -90
                       OR latitude > 90;
                    """,
                ),
                (
                    "vehicle_positions longitude should be between -180 and 180",
                    """
                    SELECT COUNT(*)
                    FROM vehicle_positions
                    WHERE longitude < -180
                       OR longitude > 180;
                    """,
                ),
                (
                    "vehicle_positions speed should not be negative",
                    """
                    SELECT COUNT(*)
                    FROM vehicle_positions
                    WHERE speed < 0;
                    """,
                ),
                (
                    "trips should not reference missing routes",
                    """
                    SELECT COUNT(*)
                    FROM trips t
                    LEFT JOIN routes r
                        ON t.route_id = r.route_id
                    WHERE r.route_id IS NULL;
                    """,
                ),
                (
                    "stop_times should not reference missing trips",
                    """
                    SELECT COUNT(*)
                    FROM stop_times st
                    LEFT JOIN trips t
                        ON st.trip_id = t.trip_id
                    WHERE t.trip_id IS NULL;
                    """,
                ),
                (
                    "stop_times should not reference missing stops",
                    """
                    SELECT COUNT(*)
                    FROM stop_times st
                    LEFT JOIN stops s
                        ON st.stop_id = s.stop_id
                    WHERE s.stop_id IS NULL;
                    """,
                ),
            ]

            for check_name, query in validation_checks:
                passed = run_zero_result_check(cursor, check_name, query)

                if passed:
                    checks_passed += 1
                else:
                    checks_failed += 1

        print("Warehouse validation completed.")
        print(f"Checks passed: {checks_passed}")
        print(f"Checks failed: {checks_failed}")

        if checks_failed > 0:
            raise ValueError("Warehouse validation failed. Check the failed validation messages above.")

    finally:
        connection.close()
        print("Database connection closed.")


def main():
    validate_warehouse()


if __name__ == "__main__":
    main()