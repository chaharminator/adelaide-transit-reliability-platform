-- Realtime Vehicle Positions Analysis
-- Purpose:
-- Analyze GTFS Realtime vehicle position records loaded into PostgreSQL.

-- 1. Total realtime vehicle position records collected
SELECT
    COUNT(*) AS total_vehicle_position_records
FROM vehicle_positions;

-- 2. Latest realtime ingestion timestamp
SELECT
    MAX(ingested_at) AS latest_ingested_at
FROM vehicle_positions;

-- 3. Latest source vehicle timestamp
SELECT
    MAX(vehicle_datetime) AS latest_vehicle_datetime
FROM vehicle_positions;

-- 4. Vehicle position records by route
SELECT
    route_id,
    COUNT(*) AS vehicle_position_records
FROM vehicle_positions
GROUP BY route_id
ORDER BY vehicle_position_records DESC
LIMIT 10;

-- 5. Unique vehicles by route
SELECT
    route_id,
    COUNT(DISTINCT vehicle_id) AS unique_vehicles
FROM vehicle_positions
WHERE vehicle_id IS NOT NULL
GROUP BY route_id
ORDER BY unique_vehicles DESC
LIMIT 10;

-- 6. Vehicles currently stopped
SELECT
    vehicle_id,
    route_id,
    trip_id,
    latitude,
    longitude,
    speed,
    vehicle_datetime,
    ingested_at
FROM vehicle_positions
WHERE speed = 0
ORDER BY ingested_at DESC
LIMIT 20;

-- 7. Average speed by route
SELECT
    route_id,
    ROUND(AVG(speed),2) AS average_speed
FROM vehicle_positions
WHERE speed IS NOT NULL
GROUP BY route_id
ORDER BY average_speed DESC
LIMIT 10;

-- 8. Latest known position for each vehicle
SELECT DISTINCT ON (vehicle_id)
    vehicle_id,
    route_id,
    trip_id,
    latitude,
    longitude,
    speed,
    bearing,
    vehicle_datetime,
    ingested_at
FROM vehicle_positions
WHERE vehicle_id IS NOT NULL
ORDER BY vehicle_id, vehicle_datetime DESC;

-- 9. Count of moving vs stopped vehicle records
SELECT
    CASE 
        WHEN speed = 0 THEN 'stopped'
        WHEN speed > 0 THEN 'moving'
        ELSE 'unknown'
    END AS movement_status,
    COUNT(*) AS record_count
FROM vehicle_positions
GROUP BY movement_status
ORDER BY record_count DESC;

-- 10. Vehicle records with missing coordinates
SELECT
    COUNT(*) AS records_missing_coordinates
FROM vehicle_positions
WHERE latitude IS NULL
    OR longitude IS NULL;