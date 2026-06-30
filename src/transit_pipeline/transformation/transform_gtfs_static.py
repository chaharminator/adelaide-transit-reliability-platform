from pathlib import Path
import pandas as pd

BRONZE_GTFS_DIR = Path("data/bronze/gtfs_static")
SILVER_GTFS_DIR = Path("data/silver/gtfs_static")

def read_gtfs_file(file_name: str) -> pd.DataFrame:
    """Read a GTFS text file from the bronze layer"""

    file_path = BRONZE_GTFS_DIR/file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Required GTFS file not found: {file_path}")
    
    return pd.read_csv(file_path)

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column name to lowercase snake_case style
    """
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ","_")
    )

    return df

def transform_routes() -> pd.DataFrame:
    """
    Transform routes.txt into a cleaned routes table.
    """
    routes = read_gtfs_file("routes.txt")
    routes = clean_column_names(routes)

    selected_columns = [
        "route_id",
        "agency_id",
        "route_short_name",
        "route_long_name",
        "route_type",
    ]

    routes = routes[selected_columns].drop_duplicates()

    return routes

def transform_stops() -> pd.DataFrame:
    """
    Transform stops.txt into a cleaned stops table.
    """
    stops = read_gtfs_file("stops.txt")
    stops = clean_column_names(stops)

    selected_columns = [
        "stop_id",
        "stop_name",
        "stop_lat",
        "stop_lon",
    ]

    stops = stops[selected_columns].drop_duplicates()

    return stops

def transform_trips() -> pd.DataFrame:
    """
    Transform trips.txt into a cleaned trips table
    """
    trips = read_gtfs_file("trips.txt")
    trips = clean_column_names(trips)

    selected_columns = [
        "route_id",
        "service_id",
        "trip_id",
        "trip_headsign",
        "direction_id",
        "shape_id",
    ]

    trips = trips[selected_columns].drop_duplicates()

    return trips

def transform_stop_times() -> pd.DataFrame:
    """Transform stop_times.txt into a cleaned stop times table."""

    stop_times = read_gtfs_file("stop_times.txt")
    stop_times = clean_column_names(stop_times)

    selected_columns = [
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence",
    ]

    stop_times = stop_times[selected_columns].drop_duplicates()

    return stop_times

def save_silver_table(df: pd.DataFrame, table_name: str) -> Path:

    """Save a transformed table into a silver layer as CSV"""

    SILVER_GTFS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = SILVER_GTFS_DIR/f"{table_name}.csv"
    df.to_csv(output_path,index = False)

    print(f"Saved {table_name}: {len(df)} rows -> {output_path}")

    return output_path

def transform_gtfs_static() -> None:
    """Run all GTFS static transformations. """

    print("Starting GTFS static transformation...")

    routes = transform_routes()
    stops = transform_stops()
    trips = transform_trips()
    stop_times = transform_stop_times()

    save_silver_table(routes, "routes")
    save_silver_table(stops, "stops")
    save_silver_table(trips, "trips")
    save_silver_table(stop_times, "stop_times")

    print("GTFS static transformation completed successfully.")

if __name__ == "__main__":
    transform_gtfs_static()