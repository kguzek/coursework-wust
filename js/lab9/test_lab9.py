import datetime
import math

import pytest

from station import Station
from timeseries import TimeSeries
from validators import (
    Analyzer,
    OutlierDetector,
    SimpleReporter,
    ThresholdDetector,
    ZeroSpikeDetector,
    detect_all_anomalies,
)


def make_station(code: str) -> Station:
    return Station(
        nr=1,
        station_code=code,
        international_code="",
        name="Test station",
        old_code="",
        start_date="",
        end_date="",
        station_type="background",
        area_type="urban",
        station_kind="automatic",
        voivodeship="dolnoslaskie",
        city="Wroclaw",
        address="Testowa 1",
        lat=51.1,
        lon=17.0,
    )


def make_series(values: list[float | None]) -> TimeSeries:
    start = datetime.datetime(2024, 1, 1, 0, 0)
    return TimeSeries(
        parameter_name="PM10",
        station_code="PL001",
        averaging_time="1g",
        dates=[start + datetime.timedelta(hours=index) for index in range(len(values))],
        values=values,
        unit="ug/m3",
    )


def test_station_eq_for_same_and_different_station_codes() -> None:
    assert make_station("PL001") == make_station("PL001")
    assert make_station("PL001") != make_station("PL002")


def test_timeseries_getitem_with_integer_index() -> None:
    series = make_series([10.0, 20.0])

    assert series[1] == (datetime.datetime(2024, 1, 1, 1, 0), 20.0)


def test_timeseries_getitem_with_slice() -> None:
    series = make_series([10.0, 20.0, 30.0])

    assert series[1:3] == [
        (datetime.datetime(2024, 1, 1, 1, 0), 20.0),
        (datetime.datetime(2024, 1, 1, 2, 0), 30.0),
    ]


def test_timeseries_getitem_with_existing_date() -> None:
    series = make_series([10.0, 20.0])

    assert series[datetime.date(2024, 1, 1)] == [10.0, 20.0]


def test_timeseries_getitem_with_missing_date_raises_key_error() -> None:
    series = make_series([10.0, 20.0])

    with pytest.raises(KeyError):
        _ = series[datetime.date(2024, 1, 2)]


def test_timeseries_mean_and_stddev_for_complete_values() -> None:
    series = make_series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])

    assert series.mean == 5.0
    assert series.stddev == 2.0


def test_timeseries_mean_and_stddev_ignore_none_values() -> None:
    series = make_series([2.0, None, 4.0, 4.0, None, 4.0, 5.0, 5.0, 7.0, 9.0])

    assert series.mean == 5.0
    assert series.stddev == 2.0


def test_outlier_detector_reports_value_farther_than_k_stddevs() -> None:
    series = make_series([10.0, 10.0, 10.0, 100.0])

    messages = OutlierDetector(k=1.0).analyze(series)

    assert len(messages) == 1
    assert "[Outlier]" in messages[0]
    assert "100.0000" in messages[0]


def test_zero_spike_detector_reports_three_consecutive_zero_or_none_values() -> None:
    series = make_series([12.0, 0.0, None, 0.0, 15.0])

    messages = ZeroSpikeDetector().analyze(series)

    assert len(messages) == 1
    assert "[ZeroSpike]" in messages[0]


def test_threshold_detector_reports_values_above_threshold() -> None:
    series = make_series([4.0, 6.0, None, 8.0])

    messages = ThresholdDetector(threshold=5.0).analyze(series)

    assert len(messages) == 2
    assert all("[Threshold]" in message for message in messages)


@pytest.mark.parametrize(
    "analyzer",
    [
        OutlierDetector(k=1.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=5.0),
        SimpleReporter(),
    ],
)
def test_detect_all_anomalies_uses_analyzer_behavior_without_type_checks(
    analyzer: Analyzer,
) -> None:
    series = make_series([0.0, None, 0.0, 10.0, 10.0, 10.0, 100.0])

    messages = detect_all_anomalies(series, [analyzer])

    assert isinstance(messages, list)
    assert all(isinstance(message, str) for message in messages)


def test_stddev_matches_population_formula() -> None:
    series = make_series([1.0, 2.0, 3.0])

    assert series.stddev == pytest.approx(math.sqrt(2 / 3))
