import datetime
import math
from dataclasses import dataclass
from typing import Self, overload


Measurement = tuple[datetime.datetime, float | None]


@dataclass
class TimeSeries:
    parameter_name: str
    station_code: str
    averaging_time: str
    dates: list[datetime.datetime]
    values: list[float | None]
    unit: str

    def __post_init__(self) -> None:
        if len(self.dates) != len(self.values):
            raise ValueError("Dates and values must have the same length")

        self.dates = list(self.dates)
        self.values = list(self.values)

    @property
    def mean(self) -> float | None:
        valid: list[float] = [value for value in self.values if value is not None]
        if not valid:
            return None
        return sum(valid) / len(valid)

    @property
    def stddev(self) -> float | None:
        valid: list[float] = [value for value in self.values if value is not None]
        count = len(valid)
        if count < 2:
            return None
        mean = sum(valid) / count
        return math.sqrt(sum((value - mean) ** 2 for value in valid) / count)

    @overload
    def __getitem__(self, key: int) -> Measurement: ...

    @overload
    def __getitem__(self, key: slice) -> list[Measurement]: ...

    @overload
    def __getitem__(self, key: datetime.datetime) -> float | None: ...

    @overload
    def __getitem__(self, key: datetime.date) -> float | None | list[float | None]: ...

    def __getitem__(
        self,
        key: int | slice | datetime.date | datetime.datetime,
    ) -> Measurement | list[Measurement] | float | None | list[float | None]:
        if isinstance(key, int):
            return self.dates[key], self.values[key]

        if isinstance(key, slice):
            return list(zip(self.dates[key], self.values[key]))

        if isinstance(key, datetime.datetime):
            for date, value in zip(self.dates, self.values):
                if date == key:
                    return value
            raise KeyError(key)

        if isinstance(key, datetime.date):
            matches: list[float | None] = [
                value for date, value in zip(self.dates, self.values) if date.date() == key
            ]
            if not matches:
                raise KeyError(key)
            return matches if len(matches) > 1 else matches[0]

        raise TypeError(f"Unsupported key type: {type(key)}")

    def __len__(self) -> int:
        return len(self.dates)

    def __repr__(self) -> str:
        return (
            f"TimeSeries(param={self.parameter_name!r}, "
            f"station={self.station_code!r}, "
            f"n={len(self.dates)})"
        )

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, TimeSeries):
            raise TypeError("Expected addition with another TimeSeries instance")

        if self.station_code != other.station_code:
            raise ValueError("Cannot merge series from different stations")
        if self.parameter_name != other.parameter_name:
            raise ValueError("Cannot merge series for different parameters")
        if self.averaging_time != other.averaging_time:
            raise ValueError("Cannot merge series with different averaging times")

        merged: list[Measurement] = sorted(
            list(zip(self.dates, self.values)) + list(zip(other.dates, other.values)),
            key=lambda item: item[0],
        )
        merged_dates: list[datetime.datetime] = [date for date, _ in merged]
        merged_values: list[float | None] = [value for _, value in merged]

        return self.__class__(
            parameter_name=self.parameter_name,
            station_code=self.station_code,
            averaging_time=self.averaging_time,
            dates=merged_dates,
            values=merged_values,
            unit=self.unit,
        )
