from collections.abc import Iterable, Iterator
import csv
from datetime import date
from pathlib import Path
from zipfile import ZipFile


type Row = dict[str, str]

COPY_COLUMNS = {
    "agency": ("agency_id", "agency_name", "agency_url", "agency_timezone", "agency_phone", "agency_lang"),
    "route_types": ("route_type2_id", "route_type2_name"),
    "vehicle_types": ("vehicle_type_id", "vehicle_type_name", "vehicle_type_description", "vehicle_type_symbol"),
    "calendar": (
        "service_id",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "start_date",
        "end_date",
    ),
    "stops": ("stop_id", "stop_code", "stop_name", "stop_lat", "stop_lon"),
    "routes": (
        "route_id",
        "agency_id",
        "route_short_name",
        "route_long_name",
        "route_desc",
        "route_type",
        "route_type2_id",
        "valid_from",
        "valid_until",
    ),
    "trips": (
        "trip_id",
        "route_id",
        "service_id",
        "trip_headsign",
        "direction_id",
        "shape_id",
        "brigade_id",
        "vehicle_id",
        "variant_id",
    ),
    "stop_times": (
        "trip_id",
        "arrival_time",
        "arrival_seconds",
        "departure_time",
        "departure_seconds",
        "stop_id",
        "stop_sequence",
        "pickup_type",
        "drop_off_type",
    ),
}

LOAD_ORDER = ("agency", "route_types", "vehicle_types", "calendar", "stops", "routes", "trips", "stop_times")
SOURCE_FILES = {
    "agency": "agency.txt",
    "route_types": "route_types.txt",
    "vehicle_types": "vehicle_types.txt",
    "calendar": "calendar.txt",
    "stops": "stops.txt",
    "routes": "routes.txt",
    "trips": "trips.txt",
    "stop_times": "stop_times.txt",
}


def rows_from_source(source: Path, filename: str) -> Iterator[Row]:
    if source.is_dir():
        with (source / filename).open(encoding="utf-8", newline="") as file_handle:
            yield from csv.DictReader(file_handle)
        return

    with ZipFile(source) as archive:
        with archive.open(filename) as file_handle:
            text_rows = (line.decode("utf-8-sig") for line in file_handle)
            yield from csv.DictReader(text_rows)


def normalize_row(table: str, row: Row) -> tuple[object, ...]:
    if table == "calendar":
        return calendar_values(row)
    if table == "trips":
        return trip_values(row)
    if table == "stop_times":
        return stop_time_values(row)
    return tuple(empty_to_none(row[column]) for column in COPY_COLUMNS[table])


def normalized_rows(source: Path, table: str) -> Iterator[tuple[object, ...]]:
    for row in rows_from_source(source, SOURCE_FILES[table]):
        yield normalize_row(table, row)


def empty_to_none(value: str) -> str | None:
    return value if value != "" else None


def parse_gtfs_date(value: str) -> date:
    if "-" in value:
        return date.fromisoformat(value)
    return date(int(value[:4]), int(value[4:6]), int(value[6:8]))


def parse_bool(value: str) -> bool:
    return value == "1"


def seconds_from_midnight(value: str) -> int:
    hours, minutes, seconds = (int(part) for part in value.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def calendar_values(row: Row) -> tuple[object, ...]:
    return (
        row["service_id"],
        parse_bool(row["monday"]),
        parse_bool(row["tuesday"]),
        parse_bool(row["wednesday"]),
        parse_bool(row["thursday"]),
        parse_bool(row["friday"]),
        parse_bool(row["saturday"]),
        parse_bool(row["sunday"]),
        parse_gtfs_date(row["start_date"]),
        parse_gtfs_date(row["end_date"]),
    )


def trip_values(row: Row) -> tuple[object, ...]:
    return tuple(empty_to_none(row[column]) for column in COPY_COLUMNS["trips"])


def stop_time_values(row: Row) -> tuple[object, ...]:
    return (
        row["trip_id"],
        row["arrival_time"],
        seconds_from_midnight(row["arrival_time"]),
        row["departure_time"],
        seconds_from_midnight(row["departure_time"]),
        row["stop_id"],
        row["stop_sequence"],
        empty_to_none(row["pickup_type"]),
        empty_to_none(row["drop_off_type"]),
    )


def batch(values: Iterable[tuple[object, ...]], size: int) -> Iterator[list[tuple[object, ...]]]:
    current: list[tuple[object, ...]] = []
    for item in values:
        current.append(item)
        if len(current) == size:
            yield current
            current = []
    if current:
        yield current
