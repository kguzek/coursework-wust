import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from timeseries import TimeSeries
from validators import SeriesValidator


@dataclass
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

    def __init__(self, directory: str | Path):
        self._dir = Path(directory)
        self._meta: list[_FileMeta] = []
        self._loaded: dict[Path, list[TimeSeries]] = {}
        self._scan()

    def _scan(self):
        for path in sorted(self._dir.glob("*.csv")):
            m = self._FNAME_RE.match(path.name)
            if not m:
                continue
            year, param, freq = m.group(1), m.group(2), m.group(3)
            station_codes = self._read_station_codes(path)
            self._meta.append(
                _FileMeta(param, freq, year, path, station_codes, len(station_codes))
            )

    @staticmethod
    def _read_station_codes(path: Path) -> list[str]:
        with open(path, encoding="utf-8") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 1:
                    return [c.strip() for c in row[1:] if c.strip()]
        return []

    def _load(self, meta: _FileMeta) -> list[TimeSeries]:
        if meta.path in self._loaded:
            return self._loaded[meta.path]

        with open(meta.path, encoding="utf-8") as f:
            rows = list(csv.reader(f))

        station_codes = [c.strip() for c in rows[1][1:]]
        indicators = [c.strip() for c in rows[2][1:]]
        avg_times = [c.strip() for c in rows[3][1:]]
        units = [c.strip() for c in rows[4][1:]]
        n = len(station_codes)

        dates: list[datetime] = []
        col_values: list[list[float | None]] = [[] for _ in range(n)]

        for row in rows[6:]:
            if not row or not row[0].strip():
                continue
            try:
                dt = datetime.strptime(row[0].strip(), self._DATE_FMT)
            except ValueError:
                continue
            dates.append(dt)
            for j in range(n):
                raw = row[j + 1].strip() if j + 1 < len(row) else ""
                col_values[j].append(float(raw) if raw else None)

        series_list = [
            TimeSeries(
                parameter_name=indicators[j] if j < len(indicators) else "",
                station_code=station_codes[j],
                averaging_time=avg_times[j] if j < len(avg_times) else "",
                dates=dates,
                values=col_values[j],
                unit=units[j] if j < len(units) else "",
            )
            for j in range(n)
        ]

        self._loaded[meta.path] = series_list
        return series_list

    def __len__(self) -> int:
        return sum(m.n_series for m in self._meta)

    def __contains__(self, parameter_name: str) -> bool:
        return any(m.param == parameter_name for m in self._meta)

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
                for ts in self._load(meta):
                    if ts.station_code == station_code:
                        result.append(ts)
        return result

    def detect_all_anomalies(
        self,
        validators: list[SeriesValidator],
        preload: bool = False,
    ) -> dict[str, list[str]]:
        if preload:
            for meta in self._meta:
                self._load(meta)

        results: dict[str, list[str]] = {}
        for series_list in self._loaded.values():
            for ts in series_list:
                messages: list[str] = []
                for v in validators:
                    messages.extend(v.analyze(ts))
                if messages:
                    key = f"{ts.station_code}/{ts.parameter_name}"
                    results.setdefault(key, []).extend(messages)

        return results

    def loaded_count(self) -> int:
        return sum(len(v) for v in self._loaded.values())
