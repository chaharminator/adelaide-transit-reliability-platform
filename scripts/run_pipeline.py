from transit_pipeline.ingestion.fetch_gtfs_static import fetch_gtfs_static
from transit_pipeline.ingestion.extract_gtfs_static import extract_gtfs_static
from transit_pipeline.transformation.transform_gtfs_static import transform_gtfs_static

def main():
    print("Starting Adelaide Transit ETL pipeline...")

    print("Step 1: Downloading GTFS static feed...")
    gtfs_zip_path = fetch_gtfs_static()

    print("Step 2: Extracting GTFS static feed...")
    extract_gtfs_static(gtfs_zip_path)

    print("Step 3: Transforming GTFS static files to silver layer...")
    transform_gtfs_static()

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()