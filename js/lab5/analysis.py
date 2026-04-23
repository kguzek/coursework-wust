"""Regex-based analyses on station data and anomaly detection."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Sequence

from models import AnomalyRecord, POLISH_TO_LATIN, Station
from parsing import parse_stations


def extract_dates(stations: Sequence[Station]) -> list[str]:
    """Extract all YYYY-MM-DD dates from station start/end fields."""
    pattern = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
    results: list[str] = []
    for s in stations:
        results.extend(pattern.findall(s.start_date))
        results.extend(pattern.findall(s.end_date))
    return results


def extract_coordinates(stations: Sequence[Station]) -> list[tuple[str, str]]:
    """Extract (latitude, longitude) pairs with 6 decimal digits."""
    pattern = re.compile(r"(\d+\.\d{6})")
    results: list[tuple[str, str]] = []
    for s in stations:
        lat_m = pattern.search(s.latitude)
        lon_m = pattern.search(s.longitude)
        if lat_m and lon_m:
            results.append((lat_m.group(1), lon_m.group(1)))
    return results


def find_hyphenated_stations(stations: Sequence[Station]) -> list[str]:
    """Find station names containing a hyphen separating two parts."""
    pattern = re.compile(r"^.+\s*-\s*.+$")
    return [s.name for s in stations if pattern.match(s.name)]


def normalize_station_names(stations: Sequence[Station]) -> list[str]:
    """Replace spaces with underscores and Polish diacritics with Latin equivalents."""
    trans = str.maketrans(POLISH_TO_LATIN)
    return [s.name.replace(" ", "_").translate(trans) for s in stations]


def verify_mob_stations(
    stations: Sequence[Station],
) -> list[tuple[str, str, bool]]:
    """Verify that all stations with codes ending in MOB have kind='mobilna'."""
    pattern = re.compile(r"MOB$")
    results: list[tuple[str, str, bool]] = []
    for s in stations:
        if pattern.search(s.code):
            is_mobile = s.kind.strip().lower() == "mobilna"
            results.append((s.code, s.kind, is_mobile))
    return results


def extract_three_part_locations(stations: Sequence[Station]) -> list[str]:
    """Find station names consisting of three hyphen-separated parts."""
    pattern = re.compile(r"^[^-]+-[^-]+-[^-]+$")
    return [s.name for s in stations if pattern.match(s.name)]


def find_locations_with_street(stations: Sequence[Station]) -> list[str]:
    """Find addresses containing a comma followed by ul. or al."""
    pattern = re.compile(r",.*(?:ul\.|al\.)")
    return [s.address for s in stations if pattern.search(s.address)]


def run_all_analyses(stations_path: Path) -> dict[str, object]:
    """Run all regex-based analyses on the stations file."""
    stations = parse_stations(stations_path)
    return {
        "dates": extract_dates(stations),
        "coordinates": extract_coordinates(stations),
        "hyphenated": find_hyphenated_stations(stations),
        "normalized_names": normalize_station_names(stations),
        "mob_verification": verify_mob_stations(stations),
        "three_part": extract_three_part_locations(stations),
        "street_locations": find_locations_with_street(stations),
    }


def _check_ratio(
    series: list[tuple[datetime, float | None]],
    station: str,
    indicator: str,
    zero_ratio_limit: float,
) -> AnomalyRecord | None:
    """Check if a station has too many null/zero/negative values."""
    total = len(series)
    bad = sum(
        1 for _, v in series if v is None or v == 0.0 or (v is not None and v < 0)
    )
    if total > 0 and bad / total > zero_ratio_limit:
        ratio = bad / total
        return AnomalyRecord(
            station_code=station,
            indicator=indicator,
            timestamp=series[0][0],
            value=None,
            reason=f"High ratio of null/zero/negative: {bad}/{total} ({ratio:.1%})",
        )
    return None


def _check_point(  # pylint: disable=too-many-arguments
    ts: datetime,
    val: float | None,
    prev_val: float | None,
    station: str,
    indicator: str,
    spike_threshold: float,
    alarm_threshold: float,
) -> list[AnomalyRecord]:
    """Check a single measurement point for anomalies."""
    found: list[AnomalyRecord] = []
    if val is not None and val < 0:
        found.append(
            AnomalyRecord(
                station_code=station,
                indicator=indicator,
                timestamp=ts,
                value=val,
                reason="Negative value",
            )
        )
    if val is not None and val > alarm_threshold:
        found.append(
            AnomalyRecord(
                station_code=station,
                indicator=indicator,
                timestamp=ts,
                value=val,
                reason=f"Value exceeds alarm threshold ({alarm_threshold})",
            )
        )
    if prev_val is not None and val is not None:
        delta = abs(val - prev_val)
        if delta > spike_threshold:
            found.append(
                AnomalyRecord(
                    station_code=station,
                    indicator=indicator,
                    timestamp=ts,
                    value=val,
                    reason=f"Spike: delta={delta:.2f} (threshold={spike_threshold})",
                )
            )
    return found


def detect_anomalies(
    measurements: list[tuple[datetime, float | None, str, str]],
    spike_threshold: float = 100.0,
    alarm_threshold: float = 500.0,
    zero_ratio_limit: float = 0.3,
) -> list[AnomalyRecord]:
    """Detect anomalies in measurement data across all stations."""
    anomalies: list[AnomalyRecord] = []
    by_station: dict[str, list[tuple[datetime, float | None]]] = {}
    indicator = measurements[0][3] if measurements else ""

    for ts, val, station, _ind in measurements:
        by_station.setdefault(station, []).append((ts, val))

    for station, series in by_station.items():
        series.sort(key=lambda x: x[0])

        ratio_anomaly = _check_ratio(series, station, indicator, zero_ratio_limit)
        if ratio_anomaly:
            anomalies.append(ratio_anomaly)

        prev_val: float | None = None
        for ts, val in series:
            anomalies.extend(
                _check_point(
                    ts,
                    val,
                    prev_val,
                    station,
                    indicator,
                    spike_threshold,
                    alarm_threshold,
                )
            )
            prev_val = val

    return anomalies
