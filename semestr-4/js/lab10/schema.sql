DROP TABLE IF EXISTS stop_times CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS stops CASCADE;
DROP TABLE IF EXISTS calendar CASCADE;
DROP TABLE IF EXISTS vehicle_types CASCADE;
DROP TABLE IF EXISTS route_types CASCADE;
DROP TABLE IF EXISTS agency CASCADE;

CREATE TABLE agency (
    agency_id integer PRIMARY KEY,
    agency_name text NOT NULL,
    agency_url text NOT NULL,
    agency_timezone text NOT NULL,
    agency_phone text,
    agency_lang text
);

CREATE TABLE route_types (
    route_type2_id integer PRIMARY KEY,
    route_type2_name text NOT NULL
);

CREATE TABLE vehicle_types (
    vehicle_type_id integer PRIMARY KEY,
    vehicle_type_name text NOT NULL,
    vehicle_type_description text,
    vehicle_type_symbol text
);

CREATE TABLE calendar (
    service_id integer PRIMARY KEY,
    monday boolean NOT NULL,
    tuesday boolean NOT NULL,
    wednesday boolean NOT NULL,
    thursday boolean NOT NULL,
    friday boolean NOT NULL,
    saturday boolean NOT NULL,
    sunday boolean NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL
);

CREATE TABLE stops (
    stop_id integer PRIMARY KEY,
    stop_code text NOT NULL,
    stop_name text NOT NULL,
    stop_lat numeric(12, 10) NOT NULL,
    stop_lon numeric(13, 10) NOT NULL
);

CREATE TABLE routes (
    route_id text PRIMARY KEY,
    agency_id integer NOT NULL REFERENCES agency(agency_id),
    route_short_name text NOT NULL,
    route_long_name text,
    route_desc text NOT NULL,
    route_type integer NOT NULL,
    route_type2_id integer REFERENCES route_types(route_type2_id),
    valid_from date NOT NULL,
    valid_until date NOT NULL
);

CREATE TABLE trips (
    trip_id text PRIMARY KEY,
    route_id text NOT NULL REFERENCES routes(route_id),
    service_id integer NOT NULL REFERENCES calendar(service_id),
    trip_headsign text NOT NULL,
    direction_id integer NOT NULL,
    shape_id integer,
    brigade_id integer,
    vehicle_id integer REFERENCES vehicle_types(vehicle_type_id),
    variant_id integer
);

CREATE TABLE stop_times (
    trip_id text NOT NULL REFERENCES trips(trip_id) ON DELETE CASCADE,
    arrival_time text NOT NULL,
    arrival_seconds integer NOT NULL,
    departure_time text NOT NULL,
    departure_seconds integer NOT NULL,
    stop_id integer NOT NULL REFERENCES stops(stop_id),
    stop_sequence integer NOT NULL,
    pickup_type integer,
    drop_off_type integer,
    PRIMARY KEY (trip_id, stop_sequence)
);

CREATE INDEX idx_routes_agency_id ON routes (agency_id);
CREATE INDEX idx_trips_route_id ON trips (route_id);
CREATE INDEX idx_trips_service_id ON trips (service_id);
CREATE INDEX idx_stop_times_stop_id ON stop_times (stop_id);
CREATE INDEX idx_stop_times_trip_id ON stop_times (trip_id);
CREATE INDEX idx_stop_times_stop_departure ON stop_times (stop_id, departure_seconds);
