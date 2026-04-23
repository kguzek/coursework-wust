"""Typer-based CLI for air quality measurement analysis."""

from __future__ import annotations

import random
import statistics
from datetime import date, datetime
from pathlib import Path

import typer

from models import VALID_FREQUENCIES, VALID_INDICATORS
from parsing import (
    group_measurement_files_by_key,
    parse_measurement_file,
    parse_stations,
)
from analysis import detect_anomalies, run_all_analyses
from cli_argparse import setup_logging, normalize_indicator, filter_rows

app = typer.Typer(help="Air quality measurement analysis tool (typer edition)")


def _validate_indicator(value: str) -> str:
    """Validate indicator name."""
    if value not in VALID_INDICATORS:
        raise typer.BadParameter(f"Unknown indicator: {value!r}")
    return value


def _validate_frequency(value: str) -> str:
    """Validate frequency value."""
    if value not in VALID_FREQUENCIES:
        raise typer.BadParameter(f"Unknown frequency: {value!r}")
    return value


def _validate_date(value: str) -> date:
    """Validate and parse a YYYY-MM-DD date string."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise typer.BadParameter(
            f"Invalid date: {value!r}. Expected YYYY-MM-DD."
        ) from exc


def _resolve(data_dir: str) -> tuple[Path, Path]:
    """Resolve and validate station/measurement paths."""
    base = Path(data_dir)
    stations = base / "stacje.csv"
    measurements = base / "measurements"
    if not stations.exists():
        typer.echo(f"Error: {stations} not found", err=True)
        raise typer.Exit(1)
    if not measurements.is_dir():
        typer.echo(f"Error: {measurements} not found", err=True)
        raise typer.Exit(1)
    return stations, measurements


def _collect_matching_codes(
    measurements_dir: Path,
    file_ind: str,
    frequency: str,
    start_d: date,
    end_d: date,
) -> set[str]:
    """Collect station codes with data matching the parameters."""
    grouped = group_measurement_files_by_key(measurements_dir)
    matching: set[str] = set()
    for key, fpath in grouped.items():
        if key.indicator != file_ind or key.frequency != frequency:
            continue
        mf = parse_measurement_file(fpath)
        for row in mf.rows:
            if not start_d <= row.timestamp.date() <= end_d:
                continue
            matching.update(c for c, v in row.values.items() if v is not None)
    return matching


@app.command()
def random_station(
    data_dir: str = typer.Option(".", help="Base data directory"),
    indicator: str = typer.Option("PM10"),
    frequency: str = typer.Option("1g"),
    start: str = typer.Option("2023-01-01", help="Start date YYYY-MM-DD"),
    end: str = typer.Option("2023-12-31", help="End date YYYY-MM-DD"),
) -> None:
    """Show a random station that measured the given indicator in the time range."""
    setup_logging()
    _validate_indicator(indicator)
    _validate_frequency(frequency)
    start_d, end_d = _validate_date(start), _validate_date(end)
    stations_path, measurements_dir = _resolve(data_dir)
    stations = parse_stations(stations_path)
    file_ind = normalize_indicator(indicator)
    matching = _collect_matching_codes(
        measurements_dir, file_ind, frequency, start_d, end_d
    )

    if not matching:
        typer.echo("No measurements found for given parameters.")
        return

    station_map = {s.code: s for s in stations}
    valid = [station_map[c] for c in matching if c in station_map]
    if not valid:
        typer.echo("No stations matched.")
        return

    chosen = random.choice(valid)
    typer.echo(f"Station: {chosen.name}")
    typer.echo(
        f"Address: {chosen.address or '(no address)'}, {chosen.city}, {chosen.voivodeship}"
    )


@app.command()
def stats(  # pylint: disable=too-many-arguments,too-many-locals
    station: str = typer.Argument(..., help="Station code"),
    data_dir: str = typer.Option(".", help="Base data directory"),
    indicator: str = typer.Option("PM10"),
    frequency: str = typer.Option("1g"),
    start: str = typer.Option("2023-01-01", help="Start date YYYY-MM-DD"),
    end: str = typer.Option("2023-12-31", help="End date YYYY-MM-DD"),
) -> None:
    """Compute mean and std dev for a station."""
    setup_logging()
    _validate_indicator(indicator)
    _validate_frequency(frequency)
    start_d, end_d = _validate_date(start), _validate_date(end)
    _, measurements_dir = _resolve(data_dir)
    grouped = group_measurement_files_by_key(measurements_dir)
    file_ind = normalize_indicator(indicator)
    values: list[float] = []

    for key, fpath in grouped.items():
        if key.indicator != file_ind or key.frequency != frequency:
            continue
        mf = parse_measurement_file(fpath)
        filtered = filter_rows(mf.rows, start_d, end_d, station_code=station)
        values.extend(v for _, v in filtered)

    if not values:
        typer.echo("No measurements found.")
        return

    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0
    typer.echo(f"Station: {station}")
    typer.echo(f"Indicator: {indicator} ({frequency})")
    typer.echo(f"Period: {start} — {end}")
    typer.echo(f"Count: {len(values)}")
    typer.echo(f"Mean: {mean:.4f}")
    typer.echo(f"Std dev: {stdev:.4f}")


def _collect_flat(  # pylint: disable=too-many-arguments
    measurements_dir: Path,
    file_ind: str,
    frequency: str,
    indicator: str,
    start_d: date,
    end_d: date,
) -> list[tuple[datetime, float | None, str, str]]:
    """Collect flat measurement tuples for anomaly detection."""
    grouped = group_measurement_files_by_key(measurements_dir)
    flat: list[tuple[datetime, float | None, str, str]] = []
    for key, fpath in grouped.items():
        if key.indicator != file_ind or key.frequency != frequency:
            continue
        mf = parse_measurement_file(fpath)
        for row in mf.rows:
            if not start_d <= row.timestamp.date() <= end_d:
                continue
            for code, val in row.values.items():
                flat.append((row.timestamp, val, code, indicator))
    return flat


@app.command()
def anomalies(
    data_dir: str = typer.Option(".", help="Base data directory"),
    indicator: str = typer.Option("PM10"),
    frequency: str = typer.Option("1g"),
    start: str = typer.Option("2023-01-01", help="Start date YYYY-MM-DD"),
    end: str = typer.Option("2023-12-31", help="End date YYYY-MM-DD"),
) -> None:
    """Detect anomalies in measurement data."""
    setup_logging()
    _validate_indicator(indicator)
    _validate_frequency(frequency)
    start_d, end_d = _validate_date(start), _validate_date(end)
    _, measurements_dir = _resolve(data_dir)
    file_ind = normalize_indicator(indicator)
    flat = _collect_flat(
        measurements_dir, file_ind, frequency, indicator, start_d, end_d
    )

    if not flat:
        typer.echo("No data found.")
        return

    results = detect_anomalies(flat)
    if not results:
        typer.echo("No anomalies detected.")
        return

    typer.echo(f"Detected {len(results)} anomalies:")
    for anomaly in results[:50]:
        typer.echo(
            f"  [{anomaly.timestamp}] {anomaly.station_code}: "
            f"{anomaly.reason} (value={anomaly.value})"
        )
    if len(results) > 50:
        typer.echo(f"  ... and {len(results) - 50} more")


@app.command()
def regex_analysis(
    data_dir: str = typer.Option(".", help="Base data directory"),
) -> None:
    """Run all regex analyses on stacje.csv (task 4)."""
    setup_logging()
    stations_path, _ = _resolve(data_dir)
    results = run_all_analyses(stations_path)

    for label, data in results.items():
        typer.echo(f"\n=== {label} ({len(data)} items) ===")
        for item in list(data)[:10]:
            typer.echo(f"  {item}")


if __name__ == "__main__":
    app()
