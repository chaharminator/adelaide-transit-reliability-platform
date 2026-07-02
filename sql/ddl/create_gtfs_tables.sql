DROP TABLE IF EXISTS stop_times;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS stops;
DROP TABLE IF EXISTS routes;

CREATE TABLE routes(
    route_id TEXT PRIMARY KEY,
    agency_id TEXT,
    route_short_name TEXT,
    route_long_name TEXT,
    route_type INTEGER
);

CREATE TABLE stops(
    stop_id TEXT PRIMARY KEY,
    stop_name TEXT,
    stop_lat NUMERIC(10,7),
    stop_lon NUMERIC(10,7)
);

CREATE TABLE trips(
    trip_id TEXT PRIMARY KEY,
    route_id TEXT,
    service_id TEXT,
    trip_headsign TEXT,
    direction_id INTEGER,
    shape_id TEXT,
    CONSTRAINT fk_trips_routes
        FOREIGN KEY(route_id)
        REFERENCES routes(route_id)
);

CREATE TABLE stop_times(
    trip_id TEXT,
    arrival_time TEXT,
    departure_time TEXT,
    stop_id TEXT,
    stop_sequence INTEGER,
    PRIMARY KEY(trip_id, stop_sequence),
    CONSTRAINT fk_stop_times_trips
        FOREIGN KEY(trip_id)
        REFERENCES trips(trip_id),
    CONSTRAINT fk_stop_times_stops
        FOREIGN KEY(stop_id)
        REFERENCES stops(stop_id)
);