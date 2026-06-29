from transit_pipeline.ingestion.fetch_gtfs_static import fetch_gtfs_static
from transit_pipeline.ingestion.extract_gtfs_static import extract_gtfs_static

def main():
    print("Starting Adelaide Transit ETL pipeline...")

    gtfs_zip_path = fetch_gtfs_static()
    extract_gtfs_static(gtfs_zip_path)

    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()