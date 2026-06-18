"""CSV parsing utilities for stations and measurement files."""

from __future__ import annotations

import csv
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Iterator

from models import (
    AddressTuple,
    MeasurementFile,
    MeasurementKey,
    MeasurementRow,
    Station,
)

logger = logging.getLogger(__name__)

_FILENAME_RE = re.compile(
    r"^(?P<year>\d{4})_(?P<indicator>.+?)_(?P<frequency>\d+[a-z]+)\.csv$"
)


def _parse_float(raw: str) -> float | None:
    """Parse a float from a string, handling Polish comma format."""
    stripped = raw.strip()
    if not stripped:
        return None
    try:
        return float(stripped.replace(",", "."))
    except ValueError:
        return None


def _count_bytes(line: str) -> int:
    """Return UTF-8 byte length of a string."""
    return len(line.encode("utf-8"))


def parse_stations(path: Path) -> list[Station]:
    """Parse the stacje.csv file into a list of Station objects."""
    logger.info("Opening file: %s", path)
    stations: list[Station] = []
    with path.open(encoding="utf-8") as fh:
        content = fh.read()
        logger.debug("Read %d bytes from %s", _count_bytes(content), path)
        lines = content.splitlines()

    actual_start = 2 if (len(lines) > 1 and not lines[1][0].isdigit()) else 1

    for line in lines[actual_start:]:
        logger.debug("Read row: %d bytes", _count_bytes(line))
        reader = csv.reader([line])
        for row in reader:
            if len(row) < 15:
                continue
            stations.append(
                Station(
                    nr=int(row[0]),
                    code=row[1],
                    international_code=row[2],
                    name=row[3],
                    old_code=row[4],
                    start_date=row[5],
                    end_date=row[6],
                    station_type=row[7],
                    area_type=row[8],
                    kind=row[9],
                    voivodeship=row[10],
                    city=row[11],
                    address=row[12],
                    latitude=row[13],
                    longitude=row[14],
                )
            )
    logger.info("Closed file: %s (parsed %d stations)", path, len(stations))
    return stations


def _parse_measurement_rows(
    rows_raw: list[list[str]],
    station_codes: list[str],
) -> list[MeasurementRow]:
    """Parse data rows from a measurement CSV into MeasurementRow objects."""
    data_rows: list[MeasurementRow] = []
    for raw_row in rows_raw:
        logger.debug("Read row: %d bytes", _count_bytes(",".join(raw_row)))
        if not raw_row or not raw_row[0].strip():
            continue
        ts = _parse_timestamp(raw_row[0])
        if ts is None:
            continue
        values: dict[str, float | None] = {}
        for i, code in enumerate(station_codes):
            val_str = raw_row[i + 1] if (i + 1) < len(raw_row) else ""
            values[code] = _parse_float(val_str)
        data_rows.append(MeasurementRow(timestamp=ts, values=values))
    return data_rows


def parse_measurement_file(path: Path) -> MeasurementFile:
    """Parse a measurement CSV file into a MeasurementFile object."""
    logger.info("Opening file: %s", path)
    with path.open(encoding="utf-8") as fh:
        content = fh.read()
    logger.debug("Read %d bytes from %s", _count_bytes(content), path)

    lines = content.splitlines()
    rows_raw = list(csv.reader(lines))

    station_codes = rows_raw[1][1:]
    indicator = rows_raw[2][1] if len(rows_raw) > 2 else ""
    frequency = rows_raw[3][1] if len(rows_raw) > 3 else ""
    unit = rows_raw[4][1] if len(rows_raw) > 4 else ""
    data_rows = _parse_measurement_rows(rows_raw[6:], station_codes)

    logger.info("Closed file: %s (parsed %d data rows)", path, len(data_rows))
    return MeasurementFile(
        station_codes=station_codes,
        indicator=indicator,
        frequency=frequency,
        unit=unit,
        rows=data_rows,
    )


def _parse_timestamp(raw: str) -> datetime | None:
    """Try multiple date formats to parse a timestamp string."""
    raw = raw.strip()
    for fmt in ("%m/%d/%y %H:%M", "%d/%m/%y %H:%M", "%Y-%m-%d %H:%M", "%m/%d/%y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def group_measurement_files_by_key(path: Path) -> dict[MeasurementKey, Path]:
    """Group measurement files in a directory by (year, indicator, frequency)."""
    result: dict[MeasurementKey, Path] = {}
    for entry in path.iterdir():
        if not entry.is_file():
            continue
        match = _FILENAME_RE.match(entry.name)
        if match:
            key = MeasurementKey(
                year=match.group("year"),
                indicator=match.group("indicator"),
                frequency=match.group("frequency"),
            )
            result[key] = entry
    return result


def get_addresses(path: Path, city: str) -> list[AddressTuple]:
    """Return addresses of stations in a given city."""
    stations = parse_stations(path)
    results: list[AddressTuple] = []
    city_re = re.compile(re.escape(city), re.IGNORECASE)

    for station in stations:
        if not city_re.search(station.city):
            continue
        addr = station.address.strip()
        if not addr:
            results.append(AddressTuple(station.voivodeship, station.city, "", None))
            continue

        street_match = re.match(r"^(.*?)(?:\s+(\d[\w/]*))?$", addr)
        if street_match:
            street = street_match.group(1).strip()
            number = street_match.group(2)
            results.append(
                AddressTuple(
                    station.voivodeship,
                    station.city,
                    street,
                    number,
                )
            )
        else:
            results.append(
                AddressTuple(
                    station.voivodeship,
                    station.city,
                    addr,
                    None,
                )
            )

    return results


def iter_all_measurements(
    measurements_dir: Path,
    indicator: str | None = None,
    frequency: str | None = None,
) -> Iterator[tuple[MeasurementFile, Path]]:
    """Iterate over parsed measurement files, optionally filtered."""
    grouped = group_measurement_files_by_key(measurements_dir)
    for key, fpath in grouped.items():
        if indicator and key.indicator != indicator:
            continue
        if frequency and key.frequency != frequency:
            continue
        yield parse_measurement_file(fpath), fpath
