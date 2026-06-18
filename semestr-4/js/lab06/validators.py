from abc import ABC, abstractmethod

from timeseries import TimeSeries


class SeriesValidator(ABC):
    @abstractmethod
    def analyze(self, series: TimeSeries) -> list[str]:
        pass


class OutlierDetector(SeriesValidator):
    def __init__(self, k: float = 3.0):
        self.k = k

    def analyze(self, series: TimeSeries) -> list[str]:
        mean = series.mean
        std = series.stddev
        if mean is None or std is None or std == 0:
            return []
        messages = []
        for dt, val in zip(series.dates, series.values):
            if val is not None and abs(val - mean) > self.k * std:
                messages.append(
                    f"[Outlier] {series.parameter_name} @ {series.station_code} "
                    f"{dt}: {val:.4f} "
                    f"(mean={mean:.4f}, std={std:.4f}, threshold=±{self.k}σ)"
                )
        return messages


class ZeroSpikeDetector(SeriesValidator):
    MIN_RUN = 3

    def analyze(self, series: TimeSeries) -> list[str]:
        messages = []
        run = 0
        run_start = None
        for i, val in enumerate(series.values):
            if val is None or val == 0:
                if run == 0:
                    run_start = i
                run += 1
            else:
                if run >= self.MIN_RUN:
                    messages.append(
                        f"[ZeroSpike] {series.parameter_name} @ {series.station_code}: "
                        f"{run} kolejnych zer/NaN od {series.dates[run_start]}"
                    )
                run = 0
                run_start = None
        if run >= self.MIN_RUN:
            messages.append(
                f"[ZeroSpike] {series.parameter_name} @ {series.station_code}: "
                f"{run} kolejnych zer/NaN od {series.dates[run_start]}"
            )
        return messages


class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float):
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> list[str]:
        messages = []
        for dt, val in zip(series.dates, series.values):
            if val is not None and val > self.threshold:
                messages.append(
                    f"[Threshold] {series.parameter_name} @ {series.station_code} "
                    f"{dt}: {val:.4f} > {self.threshold}"
                )
        return messages
