from abc import ABC, abstractmethod
from typing import Protocol

from timeseries import TimeSeries


class Analyzer(Protocol):
    def analyze(self, series: TimeSeries) -> list[str]: ...


class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        raise NotImplementedError


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float = 3.0) -> None:
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        mean = series.mean
        stddev = series.stddev
        if mean is None or stddev is None or stddev == 0:
            return []

        messages: list[str] = []
        for date, value in zip(series.dates, series.values):
            if value is not None and abs(value - mean) > self.k * stddev:
                messages.append(
                    f"[Outlier] {series.parameter_name} @ {series.station_code} "
                    f"{date}: {value:.4f} "
                    f"(mean={mean:.4f}, std={stddev:.4f}, threshold=±{self.k}σ)"
                )
        return messages


class ZeroSpikeDetector(SeriesValidator):
    MIN_RUN = 3

    def analyze(self, series: TimeSeries) -> list[str]:
        messages: list[str] = []
        run = 0
        run_start: int | None = None

        for index, value in enumerate(series.values):
            if value is None or value == 0:
                if run == 0:
                    run_start = index
                run += 1
            else:
                if run >= self.MIN_RUN and run_start is not None:
                    messages.append(
                        f"[ZeroSpike] {series.parameter_name} @ {series.station_code}: "
                        f"{run} kolejnych zer/NaN od {series.dates[run_start]}"
                    )
                run = 0
                run_start = None

        if run >= self.MIN_RUN and run_start is not None:
            messages.append(
                f"[ZeroSpike] {series.parameter_name} @ {series.station_code}: "
                f"{run} kolejnych zer/NaN od {series.dates[run_start]}"
            )
        return messages


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        messages: list[str] = []
        for date, value in zip(series.dates, series.values):
            if value is not None and value > self.threshold:
                messages.append(
                    f"[Threshold] {series.parameter_name} @ {series.station_code} "
                    f"{date}: {value:.4f} > {self.threshold}"
                )
        return messages


class SimpleReporter:
    def analyze(self, series: TimeSeries) -> list[str]:
        mean = series.mean
        mean_text = f"{mean:.4f}" if mean is not None else "brak danych"
        return [
            f"Info: {series.parameter_name} @ {series.station_code} "
            f"srednia = {mean_text} {series.unit} ({len(series)} pomiarow)"
        ]


def detect_all_anomalies(series: TimeSeries, analyzers: list[Analyzer]) -> list[str]:
    messages: list[str] = []
    for analyzer in analyzers:
        messages.extend(analyzer.analyze(series))
    return messages
