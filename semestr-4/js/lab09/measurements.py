import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from timeseries import TimeSeries
from typed_validators import Analyzer, detect_all_anomalies


@dataclass(frozen=True)
class _FileMeta:
    param: str
    freq: str
    year: str
    path: Path
    station_codes: list[str]
    n_series: int


class Measurements:
    _DATE_FMT = "%m/%d/%y %H:%M"
    _FNAME_RE = re.compile(r"^(\d{4})_(.+)_(\w+)\.csv$")

    def __init__(self, directory: str | Path) -> None:
        self._dir = Path(directory)
        self._meta: list[_FileMeta] = []
        self._loaded: dict[Path, list[TimeSeries]] = {}
        self._scan()

    def _scan(self) -> None:
        for path in sorted(self._dir.glob("*.csv")):
            match = self._FNAME_RE.match(path.name)
            if match is None:
                continue
            year, param, freq = match.group(1), match.group(2), match.group(3)
            station_codes = self._read_station_codes(path)
            self._meta.append(
                _FileMeta(param, freq, year, path, station_codes, len(station_codes))
            )

    @staticmethod
    def _read_station_codes(path: Path) -> list[str]:
        with open(path, encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 1:
                    return [code.strip() for code in row[1:] if code.strip()]
        return []

    def _load(self, meta: _FileMeta) -> list[TimeSeries]:
        if meta.path in self._loaded:
            return self._loaded[meta.path]

        with open(meta.path, encoding="utf-8", newline="") as file:
            rows = list(csv.reader(file))

        station_codes: list[str] = [code.strip() for code in rows[1][1:]]
        indicators: list[str] = [indicator.strip() for indicator in rows[2][1:]]
        avg_times: list[str] = [avg_time.strip() for avg_time in rows[3][1:]]
        units: list[str] = [unit.strip() for unit in rows[4][1:]]
        series_count = len(station_codes)

        dates: list[datetime] = []
        column_values: list[list[float | None]] = [[] for _ in range(series_count)]

        for row in rows[6:]:
            if not row or not row[0].strip():
                continue
            try:
                date = datetime.strptime(row[0].strip(), self._DATE_FMT)
            except ValueError:
                continue
            dates.append(date)
            for index in range(series_count):
                raw = row[index + 1].strip() if index + 1 < len(row) else ""
                column_values[index].append(float(raw) if raw else None)

        series_list: list[TimeSeries] = [
            TimeSeries(
                parameter_name=indicators[index] if index < len(indicators) else "",
                station_code=station_codes[index],
                averaging_time=avg_times[index] if index < len(avg_times) else "",
                dates=dates,
                values=column_values[index],
                unit=units[index] if index < len(units) else "",
            )
            for index in range(series_count)
        ]

        self._loaded[meta.path] = series_list
        return series_list

    def __len__(self) -> int:
        return sum(meta.n_series for meta in self._meta)

    def __contains__(self, parameter_name: object) -> bool:
        if not isinstance(parameter_name, str):
            return False
        return any(meta.param == parameter_name for meta in self._meta)

    def get_by_parameter(self, param_name: str) -> list[TimeSeries]:
        result: list[TimeSeries] = []
        for meta in self._meta:
            if meta.param == param_name:
                result.extend(self._load(meta))
        return result

    def get_by_station(self, station_code: str) -> list[TimeSeries]:
        result: list[TimeSeries] = []
        for meta in self._meta:
            if station_code in meta.station_codes:
                result.extend(
                    series
                    for series in self._load(meta)
                    if series.station_code == station_code
                )
        return result

    def detect_all_anomalies(
        self,
        analyzers: list[Analyzer],
        preload: bool = False,
    ) -> dict[str, list[str]]:
        if preload:
            for meta in self._meta:
                self._load(meta)

        results: dict[str, list[str]] = {}
        for series_list in self._loaded.values():
            for series in series_list:
                messages = detect_all_anomalies(series, analyzers)
                if messages:
                    key = f"{series.station_code}/{series.parameter_name}"
                    results.setdefault(key, []).extend(messages)
        return results

    def loaded_count(self) -> int:
        return sum(len(series_list) for series_list in self._loaded.values())
