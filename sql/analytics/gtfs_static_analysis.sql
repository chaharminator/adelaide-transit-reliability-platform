-- ============================================================
-- GTFS Static Schedule Analysis
-- Purpose:
-- Validate the PostgreSQL warehouse tables and generate
-- first-level schedule insights from Adelaide Metro GTFS data.
-- ============================================================

SELECT 'routes' AS table_name, COUNT(*) AS row_count FROM routes
UNION ALL
SELECT 'stops' AS table_name, COUNT(*) AS row_count FROM stops
UNION ALL
SELECT 'trips' AS table_name, COUNT(*) AS row_count FROM trips
UNION ALL
SELECT 'stop_times' AS table_name, COUNT(*) AS row_count FROM stop_times;

--2. Top routes by number of scheduled trips
SELECT  
    r.route_short_name,
    r.route_long_name,
    COUNT(DISTINCT t.trip_id) AS total_scheduled_trips
FROM routes r
JOIN trips t
    ON r.route_id = t.route_id
GROUP BY
    r.route_short_name,
    r.route_long_name
ORDER BY total_scheduled_trips DESC
LIMIT 10;

--3. Top stops by number of scheduled stop events
SELECT
    s.stop_id,
    s.stop_name,
    COUNT(*) AS total_scheduled_stop_events
FROM stop_times st
JOIN stops s
    ON st.stop_id = s.stop_id
GROUP BY 
    s.stop_id,
    s.stop_name
ORDER BY total_scheduled_stop_events DESC
LIMIT 10;

--4. Trips with the highest number of stops
SELECT
    t.trip_id,
    r.route_short_name,
    r.route_long_name,
    COUNT(st.stop_id) AS total_stops
FROM trips t
JOIN routes r
    ON t.route_id = r.route_id
JOIN stop_times st
    ON t.trip_id = st.trip_id
GROUP BY
    t.trip_id,
    r.route_short_name,
    r.route_long_name
ORDER BY total_stops DESC
LIMIT 10;

--5. Route level total scheduled stop events
SELECT  
    r.route_short_name,
    r.route_long_name,
    COUNT(*) AS total_scheduled_stop_events
FROM routes r
JOIN trips t
    ON r.route_id = t.route_id
JOIN stop_times st
    ON t.trip_id = st.trip_id
GROUP BY 
    r.route_short_name,
    r.route_long_name
ORDER BY total_scheduled_stop_events DESC
LIMIT 10;

--6. Route type distribution
SELECT  
    route_type,
    COUNT(*) AS total_routes
FROM routes
GROUP BY route_type
ORDER BY total_routes DESC;