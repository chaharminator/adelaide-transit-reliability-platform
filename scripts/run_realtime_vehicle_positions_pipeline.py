from transit_pipeline.transformation.transform_gtfs_realtime import transform_vehicle_positions
from transit_pipeline.loading.load_realtime_to_postgres import load_realtime_to_postgres

def main():
    print("Starting Adelaide Transit realtime vehicle positions pipeline...")

    print("Step 1: Fetching and transforming realtime vehicle positions...")
    transform_vehicle_positions()

    print("Step 2: Loading realtime vehicle positions into PostgreSQL...")
    load_realtime_to_postgres()

    print("Realtime vehicle positions pipeline completed successfully.")

if __name__ == "__main__":
    main()