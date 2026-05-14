import datetime
import math
from typing import Self, Union


class TimeSeries:
    def __init__(
        self,
        parameter_name: str,
        station_code: str,
        averaging_time: str,
        dates: list[datetime.datetime],
        values: list[float | None],
        unit: str,
    ):
        self.parameter_name = parameter_name
        self.station_code = station_code
        self.averaging_time = averaging_time
        self._dates = list(dates)
        self._values = list(values)
        self.unit = unit

    @property
    def dates(self) -> list[datetime.datetime]:
        return self._dates

    @property
    def values(self) -> list[float | None]:
        return self._values

    @property
    def mean(self) -> float | None:
        valid = [v for v in self._values if v is not None]
        if not valid:
            return None
        return sum(valid) / len(valid)

    @property
    def stddev(self) -> float | None:
        valid = [v for v in self._values if v is not None]
        n = len(valid)
        if n < 2:
            return None
        m = sum(valid) / n
        return math.sqrt(sum((x - m) ** 2 for x in valid) / n)

    def __getitem__(
        self,
        key: Union[int, slice, datetime.date, datetime.datetime],
    ):
        if isinstance(key, int):
            return (self._dates[key], self._values[key])

        if isinstance(key, slice):
            return [(d, v) for d, v in zip(self._dates[key], self._values[key])]

        if isinstance(key, datetime.datetime):
            for d, v in zip(self._dates, self._values):
                if d == key:
                    return v
            raise KeyError(key)

        if isinstance(key, datetime.date):
            matches = [v for d, v in zip(self._dates, self._values) if d.date() == key]
            if not matches:
                raise KeyError(key)
            return matches if len(matches) > 1 else matches[0]

        raise TypeError(f"Unsupported key type: {type(key)}")

    def __len__(self) -> int:
        return len(self._dates)

    def __repr__(self) -> str:
        return (
            f"TimeSeries(param={self.parameter_name!r}, "
            f"station={self.station_code!r}, "
            f"n={len(self._dates)})"
        )

    def __add__(self, other) -> Self:
        if not isinstance(other, TimeSeries):
            raise TypeError("Expected addition with another TimeSeries instance")

        if self.station_code != other.station_code:
            raise ValueError("Cannot merge series from different stations")
        if self.parameter_name != other.parameter_name:
            raise ValueError("Cannot merge series for different parameters")
        if self.averaging_time != other.averaging_time:
            raise ValueError("Cannot merge series with different averaging times")

        merged = sorted(
            list(zip(self._dates, self._values))
            + list(zip(other._dates, other._values)),
            key=lambda x: x[0],
        )
        merged_dates = [d for d, _ in merged]
        merged_values = [v for _, v in merged]

        return TimeSeries(
            parameter_name=self.parameter_name,
            station_code=self.station_code,
            averaging_time=self.averaging_time,
            dates=merged_dates,
            values=merged_values,
            unit=self.unit,
        )
