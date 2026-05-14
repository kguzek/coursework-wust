import datetime
from pathlib import Path

from station import Station, load_stations
from timeseries import TimeSeries
from validators import (
    SeriesValidator,
    OutlierDetector,
    ZeroSpikeDetector,
    ThresholdDetector,
)
from measurements import Measurements


# kacze typowanie - SimpleReporter nie dziedziczy po SeriesValidator
class SimpleReporter:
    def analyze(self, series: TimeSeries) -> list[str]:
        mean = series.mean
        mean_str = f"{mean:.4f}" if mean is not None else "brak danych"
        return [
            f"Info: {series.parameter_name} @ {series.station_code} "
            f"srednia = {mean_str} {series.unit} "
            f"({len(series)} pomiarow)"
        ]


def main():
    base = Path(__file__).parent

    # --- zadanie 1: Station ---
    print("\n=== Zadanie 1 – klasa Station ===")

    stations = load_stations(base / "stacje.csv")
    sample_codes = list(stations.keys())[:3]
    for code in sample_codes:
        s = stations[code]
        print(f"  str:  {s}")
        print(f"  repr: {s!r}")

    s1 = stations[sample_codes[0]]
    s2 = Station(
        nr=s1.nr,
        station_code=s1.station_code,
        international_code="",
        name="kopia",
        old_code="",
        start_date="",
        end_date="",
        station_type="",
        area_type="",
        station_kind="",
        voivodeship="",
        city="",
        address="",
        lat=None,
        lon=None,
    )
    print(f"\n  s1 == s2 (ten sam kod): {s1 == s2}")
    print(f"  s1 == stations['{sample_codes[1]}']: {s1 == stations[sample_codes[1]]}")

    # --- zadanie 2 i 3: TimeSeries + wlasciwosci ---
    print("\n=== Zadania 2 & 3 – TimeSeries, mean, stddev ===")

    meas = Measurements(base / "measurements")

    c6h6_series = meas.get_by_parameter("C6H6")
    ts = c6h6_series[0]
    print(f"  {ts!r}")
    print(f"  srednia = {ts.mean:.6f} {ts.unit}")
    std = ts.stddev
    print(f"  odch. std = {std:.6f} {ts.unit}" if std else "  odch. std = brak")

    # indeks
    print(f"\n  ts[0] = {ts[0]}")
    print(f"  ts[1:4] = {ts[1:4]}")

    # datetime.datetime - dokladny timestamp
    dt_exact = ts.dates[5]
    print(f"\n  ts[{dt_exact}] = {ts[dt_exact]}")

    # datetime.date - wszystkie wartosci z danego dnia
    day = ts.dates[0].date()
    result = ts[day]
    print(
        f"  ts[{day}] -> {result if not isinstance(result, list) else f'{len(result)} wartosci'}"
    )

    # KeyError dla nieistniejacego znacznika
    try:
        ts[datetime.datetime(2000, 1, 1, 0, 0)]
    except KeyError as e:
        print(f"  KeyError (brak znacznika): {e}")

    # --- zadanie 4 i 6: walidatory + detect_all_anomalies ---
    print("\n=== Zadania 4 & 6 – walidatory, wykrywanie anomalii ===")

    validators = [
        OutlierDetector(k=4.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=5.0),
    ]

    anomalies = meas.detect_all_anomalies(validators, preload=False)

    total = sum(len(v) for v in anomalies.values())
    print(
        f"  znaleziono anomalie w {len(anomalies)} seriach, lacznie {total} komunikatow"
    )

    for key, msgs in list(anomalies.items())[:2]:
        print(f"\n  [{key}]")
        for msg in msgs[:3]:
            print(f"    {msg}")
        if len(msgs) > 3:
            print(f"    ... (jeszcze {len(msgs) - 3})")

    # --- zadanie 5: interfejs Measurements ---
    print("\n=== Zadanie 5 – klasa Measurements ===")

    print(f"  liczba mozliwych do zaladowania TimeSeries: {len(meas)}")
    print(f"  'C6H6' in meas: {'C6H6' in meas}")
    print(f"  'XYZ' in meas:  {'XYZ' in meas}")

    station_code = ts.station_code
    by_station = meas.get_by_station(station_code)
    print(f"\n  serie dla stacji {station_code!r}: {len(by_station)} sztuk")
    for s in by_station[:4]:
        print(f"    {s!r}")

    # --- zadanie 8: kacze typowanie ---
    print("\n=== Zadanie 8 – kacze typowanie (duck typing) ===")

    sample_ts = c6h6_series[1]

    # lista analizatorow - mix podklas SeriesValidator i SimpleReporter
    analyzers = [
        OutlierDetector(k=3.0),
        ZeroSpikeDetector(),
        ThresholdDetector(threshold=2.0),
        SimpleReporter(),  # nie dziedziczy po SeriesValidator!
    ]

    print(f"  analizowana seria: {sample_ts!r}\n")
    for analyzer in analyzers:
        # bez isinstance / hasattr - czyste kacze typowanie
        messages = analyzer.analyze(sample_ts)
        kind = type(analyzer).__name__
        print(f"  [{kind}] -> {len(messages)} komunikat(ow)")
        for msg in messages[:2]:
            print(f"      {msg}")
        if len(messages) > 2:
            print(f"      ... (jeszcze {len(messages) - 2})")

    print(
        f"\n  czy SimpleReporter dziedziczy po SeriesValidator: {issubclass(SimpleReporter, SeriesValidator)}"
    )
    print("  mimo to dziala identycznie - to jest wlasnie kacze typowanie")

    # --- zadanie 7: operator + dla TimeSeries ---
    print("\n=== Zadanie 7 – operator + dla TimeSeries ===")

    base_dates = [
        datetime.datetime(2024, 1, 1, 0, 0),
        datetime.datetime(2024, 1, 1, 1, 0),
    ]
    extra_dates = [
        datetime.datetime(2024, 1, 1, 2, 0),
        datetime.datetime(2024, 1, 1, 3, 0),
    ]

    series1 = TimeSeries(
        parameter_name="NO2",
        station_code="PL001",
        averaging_time="1g",
        dates=base_dates,
        values=[10.0, 12.5],
        unit="ug/m3",
    )
    series2 = TimeSeries(
        parameter_name="NO2",
        station_code="PL001",
        averaging_time="1g",
        dates=extra_dates,
        values=[11.0, 9.5],
        unit="ug/m3",
    )

    series3 = series1 + series2
    print(f"  seria wynikowa: {series3!r}")
    print(f"  liczba pomiarow: {len(series3)}")
    print(f"  pierwszy punkt: {series3[0]}")
    print(f"  ostatni punkt: {series3[-1]}")

    try:
        bad_station = TimeSeries(
            parameter_name="NO2",
            station_code="PL999",
            averaging_time="1g",
            dates=extra_dates,
            values=[1.0, 2.0],
            unit="ug/m3",
        )
        _ = series1 + bad_station
    except ValueError as e:
        print(f"  ValueError (rozne stacje): {e}")

    try:
        bad_param = TimeSeries(
            parameter_name="SO2",
            station_code="PL001",
            averaging_time="1g",
            dates=extra_dates,
            values=[1.0, 2.0],
            unit="ug/m3",
        )
        _ = series1 + bad_param
    except ValueError as e:
        print(f"  ValueError (rozne wskazniki): {e}")

    try:
        bad_avg = TimeSeries(
            parameter_name="NO2",
            station_code="PL001",
            averaging_time="24g",
            dates=extra_dates,
            values=[1.0, 2.0],
            unit="ug/m3",
        )
        _ = series1 + bad_avg
    except ValueError as e:
        print(f"  ValueError (rozny czas usredniania): {e}")


if __name__ == "__main__":
    main()
