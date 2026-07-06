from pathlib import Path
from datetime import datetime, timezone
import requests
from google.transit import gtfs_realtime_pb2

VEHICLE_POSITIONS_URL = "https://gtfs.adelaidemetro.com.au/v1/realtime/vehicle_positions"

def fetch_vehicle_positions(output_dir: str = "data/raw/gtfs_realtime") -> Path:
    """
    Download Adelaide Metro GTFS Realtime vehicle positions feed
    and save the raw protobuf response locally
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_path = output_path/f"vehicle_positions_{timestamp}.pb"

    print("Starting GTFS Realtime vehicle positions download...")
    print(f"Source URL: {VEHICLE_POSITIONS_URL}")

    response = requests.get(VEHICLE_POSITIONS_URL, timeout=60)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)

    print(f"Download Completed: {file_path}")
    print(f"File size: {file_path.stat().st_size/1024:.2f} KB")

    return file_path

def parse_vehicle_positions(pb_file_path: Path) -> list[dict]:
    """
    Parse a GTFS Realtime vehicle positions protobuf file
    into a list of Python dictionaties.
    """

    feed = gtfs_realtime_pb2.FeedMessage()

    with open(pb_file_path, "rb") as file:
        feed.ParseFromString(file.read())
    
    vehicle_records = []

    for entity in feed.entity:
        if not entity.HasField("vehicle"):
            continue

        vehicle = entity.vehicle

        record = {
            "entity_id": entity.id,
            "trip_id": vehicle.trip.trip_id if vehicle.HasField("trip") else None,
            "route_id": vehicle.trip.route_id if vehicle.HasField("trip") else None,
            "vehicle_id": vehicle.vehicle.id if vehicle.HasField("vehicle") else None,
            "vehicle_label": vehicle.vehicle.label if vehicle.HasField("vehicle") else None,
            "latitude": vehicle.position.latitude if vehicle.HasField("position") else None,
            "longitude": vehicle.position.longitude if vehicle.HasField("position") else None,
            "bearing": vehicle.position.bearing if vehicle.HasField("position") else None,
            "speed": vehicle.position.speed if vehicle.HasField("position") else None,
            "timestamp": vehicle.timestamp if vehicle.timestamp else None,
        }

        vehicle_records.append(record)

    print(f"Parsed {len(vehicle_records)} vehicle position records.")

    return vehicle_records

def main():
    pb_file_path = fetch_vehicle_positions()
    vehicle_records = parse_vehicle_positions(pb_file_path)

    print("Sample records:")
    for record in vehicle_records[:5]:
        print(record)

if __name__ == "__main__":
    main()