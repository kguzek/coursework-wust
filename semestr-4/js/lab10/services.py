from decimal import Decimal
from typing import TypedDict

from psycopg.rows import dict_row

from db import connect


class StopChoice(TypedDict):
    stop_id: int
    stop_code: str
    stop_name: str


class StopPreview(TypedDict):
    stop_id: int
    stop_code: str
    stop_name: str
    stop_lat: float
    stop_lon: float
    lines: int
    bus_lines: int
    tram_lines: int
    night_lines: int
    departures: int


class DirectionCount(TypedDict):
    trip_headsign: str
    departures: int


class RouteCount(TypedDict):
    route_short_name: str
    route_type: int
    departures: int


class StopStats(TypedDict):
    stop: StopChoice
    distinct_lines: int
    departures: int
    earliest_departure: str | None
    latest_departure: str | None
    common_directions: list[DirectionCount]
    busiest_routes: list[RouteCount]
    average_departures_per_line: Decimal | None


def search_stops(query: str, database: str | None = None, limit: int = 25) -> list[StopChoice]:
    pattern = f"%{query}%"
    statement = """
        SELECT stop_id, stop_code, stop_name
        FROM stops
        WHERE stop_name ILIKE %(pattern)s OR stop_code ILIKE %(pattern)s OR stop_id::text = %(query)s
        ORDER BY stop_name, stop_code
        LIMIT %(limit)s
    """
    with connect(database) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(statement, {"pattern": pattern, "query": query, "limit": limit})
            return [StopChoice(row) for row in cursor.fetchall()]


def search_stops_preview(query: str, database: str | None = None, limit: int = 25) -> list[StopPreview]:
    pattern = f"%{query}%"
    statement = """
        SELECT
            s.stop_id,
            s.stop_code,
            s.stop_name,
            s.stop_lat,
            s.stop_lon,
            count(DISTINCT r.route_id) AS lines,
            count(DISTINCT r.route_id) FILTER (WHERE rt.route_type2_name ILIKE '%%autobusowa%%') AS bus_lines,
            count(DISTINCT r.route_id) FILTER (WHERE rt.route_type2_name ILIKE '%%tramwajowa%%') AS tram_lines,
            count(DISTINCT r.route_id) FILTER (WHERE rt.route_type2_name ILIKE '%%nocna%%') AS night_lines,
            count(*) AS departures
        FROM stops s
        LEFT JOIN stop_times st ON st.stop_id = s.stop_id
        LEFT JOIN trips t ON t.trip_id = st.trip_id
        LEFT JOIN routes r ON r.route_id = t.route_id
        LEFT JOIN route_types rt ON rt.route_type2_id = r.route_type2_id
        WHERE s.stop_name ILIKE %(pattern)s OR s.stop_code ILIKE %(pattern)s OR s.stop_id::text = %(query)s
        GROUP BY s.stop_id, s.stop_code, s.stop_name
        ORDER BY s.stop_name, s.stop_code
        LIMIT %(limit)s
    """
    with connect(database) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(statement, {"pattern": pattern, "query": query, "limit": limit})
            return [StopPreview(row) for row in cursor.fetchall()]


def stop_by_id(stop_id: int, database: str | None = None) -> StopChoice:
    with connect(database) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT stop_id, stop_code, stop_name FROM stops WHERE stop_id = %s", (stop_id,))
            row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Stop {stop_id} does not exist")
    return StopChoice(row)


def stop_statistics(stop_id: int, database: str | None = None) -> StopStats:
    stop = stop_by_id(stop_id, database)
    with connect(database) as connection:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(SUMMARY_SQL, (stop_id, stop_id))
            summary = cursor.fetchone()
            cursor.execute(COMMON_DIRECTIONS_SQL, (stop_id,))
            directions = [DirectionCount(row) for row in cursor.fetchall()]
            cursor.execute(BUSIEST_ROUTES_SQL, (stop_id,))
            routes = [RouteCount(row) for row in cursor.fetchall()]
            cursor.execute(AVERAGE_DEPARTURES_SQL, (stop_id,))
            average = cursor.fetchone()

    if summary is None or average is None:
        raise ValueError(f"Stop {stop_id} does not exist")

    return StopStats(
        stop=stop,
        distinct_lines=int(summary["distinct_lines"]),
        departures=int(summary["departures"]),
        earliest_departure=summary["earliest_departure"],
        latest_departure=summary["latest_departure"],
        common_directions=directions,
        busiest_routes=routes,
        average_departures_per_line=average["average_departures_per_line"],
    )


SUMMARY_SQL = """
    SELECT
        count(DISTINCT r.route_id) AS distinct_lines,
        count(*) AS departures,
        min(st.departure_time) FILTER (WHERE st.departure_seconds = bounds.min_seconds) AS earliest_departure,
        max(st.departure_time) FILTER (WHERE st.departure_seconds = bounds.max_seconds) AS latest_departure
    FROM stop_times st
    JOIN trips t ON t.trip_id = st.trip_id
    JOIN routes r ON r.route_id = t.route_id
    CROSS JOIN (
        SELECT min(departure_seconds) AS min_seconds, max(departure_seconds) AS max_seconds
        FROM stop_times
        WHERE stop_id = %s
    ) bounds
    WHERE st.stop_id = %s
"""

COMMON_DIRECTIONS_SQL = """
    SELECT t.trip_headsign, count(*) AS departures
    FROM stop_times st
    JOIN trips t ON t.trip_id = st.trip_id
    WHERE st.stop_id = %s
    GROUP BY t.trip_headsign
    ORDER BY departures DESC, t.trip_headsign
    LIMIT 5
"""

BUSIEST_ROUTES_SQL = """
    SELECT r.route_short_name, r.route_type, count(*) AS departures
    FROM stop_times st
    JOIN trips t ON t.trip_id = st.trip_id
    JOIN routes r ON r.route_id = t.route_id
    WHERE st.stop_id = %s
    GROUP BY r.route_short_name, r.route_type
    ORDER BY departures DESC, r.route_short_name
    LIMIT 10
"""

AVERAGE_DEPARTURES_SQL = """
    SELECT avg(route_departures.departures) AS average_departures_per_line
    FROM (
        SELECT r.route_id, count(*) AS departures
        FROM stop_times st
        JOIN trips t ON t.trip_id = st.trip_id
        JOIN routes r ON r.route_id = t.route_id
        WHERE st.stop_id = %s
        GROUP BY r.route_id
    ) route_departures
"""
