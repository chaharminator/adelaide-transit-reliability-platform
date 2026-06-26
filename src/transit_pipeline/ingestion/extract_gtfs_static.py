from pathlib import Path
import zipfile

def get_latest_gtfs_zip(raw_dir: str = "data/raw") -> Path:
    """
    Find the latest GTFS static zip file from the raw data folder
    """

    raw_path = Path(raw_dir)

    zip_files = list(raw_path.glob("adelaide_gtfs_static_*.zip"))
    if not zip_files:
        raise FileNotFoundError("No GTFS static zip files found in data/raw.")
    
    latest_zip = max(zip_files, key=lambda file: file.stat().st_mtime)
    return latest_zip

def extract_gtfs_static(
        zip_file_path: Path,
        output_dir: str = "data/bronze/gtfs_static",
) -> Path:
    """Extract the GTFS static ZIP file into bronze layer
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Extracting file: {zip_file_path}")
    print(f"Output folder: {output_path}")

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(output_path)
    
    extracted_files = sorted([file.name for file in output_path.iterdir()])

    print("Extraction completed:")
    print("Files extracted:")

    for file_name in extracted_files:
        print(f"- {file_name}")
    return output_path

def main():
    latest_zip = get_latest_gtfs_zip()
    extract_gtfs_static(latest_zip)

if __name__ == "__main__":
    main()
