"""Data models for air quality measurement analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import NamedTuple


class MeasurementKey(NamedTuple):
    """Key identifying a measurement file by year, indicator, and frequency."""

    year: str
    indicator: str
    frequency: str


class AddressTuple(NamedTuple):
    """Station address components."""

    voivodeship: str
    city: str
    street: str
    number: str | None


@dataclass(frozen=True, slots=True)
class Station:  # pylint: disable=too-many-instance-attributes
    """A single measurement station parsed from stacje.csv."""

    nr: int
    code: str
    international_code: str
    name: str
    old_code: str
    start_date: str
    end_date: str
    station_type: str
    area_type: str
    kind: str
    voivodeship: str
    city: str
    address: str
    latitude: str
    longitude: str


@dataclass(slots=True)
class MeasurementFile:
    """Parsed content of a single measurement CSV file."""

    station_codes: list[str]
    indicator: str
    frequency: str
    unit: str
    rows: list[MeasurementRow] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class MeasurementRow:
    """Single timestamped row of measurements across stations."""

    timestamp: datetime
    values: dict[str, float | None]


@dataclass(frozen=True, slots=True)
class AnomalyRecord:
    """A detected anomaly in measurement data."""

    station_code: str
    indicator: str
    timestamp: datetime
    value: float | None
    reason: str


POLISH_TO_LATIN: dict[str, str] = {
    "ą": "a",
    "ć": "c",
    "ę": "e",
    "ł": "l",
    "ń": "n",
    "ó": "o",
    "ś": "s",
    "ź": "z",
    "ż": "z",
    "Ą": "A",
    "Ć": "C",
    "Ę": "E",
    "Ł": "L",
    "Ń": "N",
    "Ó": "O",
    "Ś": "S",
    "Ź": "Z",
    "Ż": "Z",
}

VALID_INDICATORS: frozenset[str] = frozenset(
    {
        "PM10",
        "PM25",
        "PM2.5",
        "NO",
        "NO2",
        "NOx",
        "SO2",
        "CO",
        "O3",
        "C6H6",
        "As(PM10)",
        "BaP(PM10)",
        "BaA(PM10)",
        "BbF(PM10)",
        "BjF(PM10)",
        "BkF(PM10)",
        "Cd(PM10)",
        "DBahA(PM10)",
        "IP(PM10)",
        "Ni(PM10)",
        "Pb(PM10)",
        "Hg(TGM)",
        "formaldehyd",
        "Depozycja",
        "Jony_PM25",
        "PrekursoryZielonka",
    }
)

VALID_FREQUENCIES: frozenset[str] = frozenset({"1g", "24g", "1m"})
