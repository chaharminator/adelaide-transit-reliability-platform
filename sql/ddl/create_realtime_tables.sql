DROP TABLE IF EXISTS vehicle_positions;

CREATE TABLE vehicle_positions (
    position_id BIGSERIAL PRIMARY KEY,

    entity_id TEXT,
    trip_id TEXT,
    route_id TEXT,
    vehicle_id TEXT,
    vehicle_label TEXT,

    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    bearing NUMERIC(10, 4),
    speed NUMERIC(10, 4),

    vehicle_timestamp BIGINT,
    vehicle_datetime TIMESTAMP,

    ingestion_file TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);