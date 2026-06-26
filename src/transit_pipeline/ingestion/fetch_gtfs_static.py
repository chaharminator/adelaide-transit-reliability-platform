from pathlib import Path
from datetime import datetime
import requests

GTFS_STATIC_URL = "https://gtfs.adelaidemetro.com.au/v1/static/latest/google_transit.zip"

def fetch_gtfs_static(output_dir: str = "data/raw") -> Path:
    """
    Download latest Adelaide Metro GTFS static feed.
    output_dir: Local folder where downloaded zip file will be saved.
    returns: Path to downloaded zip file.
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents = True, exist_ok = True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_path / f"adelaide_gtfs_static_{timestamp}.zip"

    print("Starting GTFS static feed download...")
    print(f"Source URL: {GTFS_STATIC_URL}")

    response = requests.get(GTFS_STATIC_URL, timeout=60)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"Download completed: {file_path}")
    print(f"File size: {file_path.stat().st_size/1024/1024:.2f} MB")

    return file_path