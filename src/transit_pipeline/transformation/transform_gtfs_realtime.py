from pathlib import Path
import pandas as pd

from transit_pipeline.ingestion.fetch_gtfs_realtime import (
    fetch_vehicle_positions,
    parse_vehicle_positions,
)


SILVER_REALTIME_DIR = Path("data/silver/gtfs_realtime")


def transform_vehicle_positions() -> Path:
    """
    Fetch GTFS Realtime vehicle positions, parse the protobuf feed,
    clean the records, and save them as a silver-layer CSV file.
    """
    SILVER_REALTIME_DIR.mkdir(parents=True, exist_ok=True)

    pb_file_path = fetch_vehicle_positions()
    vehicle_records = parse_vehicle_positions(pb_file_path)

    df = pd.DataFrame(vehicle_records)

    if df.empty:
        raise ValueError("No vehicle position records found in GTFS Realtime feed.")

    df["ingestion_file"] = pb_file_path.name

    output_file_path = SILVER_REALTIME_DIR / "vehicle_positions.csv"
    df.to_csv(output_file_path, index=False)

    print(f"Saved silver vehicle positions: {output_file_path}")
    print(f"Total records saved: {len(df)}")

    return output_file_path


def main():
    transform_vehicle_positions()


if __name__ == "__main__":
    main()