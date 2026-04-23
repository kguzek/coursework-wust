"""Argparse-based CLI for air quality measurement analysis."""

from __future__ import annotations

import argparse
import logging
import random
import statistics
import sys
from datetime import date, datetime
from pathlib import Path

from models import VALID_FREQUENCIES, VALID_INDICATORS, MeasurementRow
from parsing import (
    group_measurement_files_by_key,
    parse_measurement_file,
    parse_stations,
)
from analysis import detect_anomalies, run_all_analyses

logger = logging.getLogger("air_quality")


class _StdoutFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    """Filter that passes only records below ERROR level."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno < logging.ERROR


def setup_logging() -> None:
    """Configure logging: DEBUG-WARNING to stdout, ERROR+ to stderr."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(_StdoutFilter())
    stdout_handler.setFormatter(fmt)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(fmt)

    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)


def _valid_date(value: str) -> date:
    """Validate and parse a YYYY-MM-DD date string for argparse."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"Invalid date: {value!r}. Expected YYYY-MM-DD."
        ) from exc


def _valid_indicator(value: str) -> str:
    """Validate an indicator name for argparse."""
    if value not in VALID_INDICATORS:
        raise argparse.ArgumentTypeError(
            f"Unknown indicator: {value!r}. Valid: {', '.join(sorted(VALID_INDICATORS))}"
        )
    return value


def _valid_frequency(value: str) -> str:
    """Validate a frequency value for argparse."""
    if value not in VALID_FREQUENCIES:
        raise argparse.ArgumentTypeError(
            f"Unknown frequency: {value!r}. Valid: {', '.join(sorted(VALID_FREQUENCIES))}"
        )
    return value


def _resolve_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    """Resolve and validate station/measurement paths from CLI args."""
    base = Path(args.data_dir)
    stations_path = base / "stacje.csv"
    measurements_dir = base / "measurements"
    if not stations_path.exists():
        logger.error("Stations file not found: %s", stations_path)
        sys.exit(1)
    if not measurements_dir.is_dir():
        logger.error("Measurements directory not found: %s", measurements_dir)
        sys.exit(1)
    return stations_path, measurements_dir


def normalize_indicator(indicator: str) -> str:
    """Normalize indicator name to match filenames (e.g. PM2.5 -> PM25)."""
    return indicator.replace(".", "").replace("PM2.5", "PM25")


def filter_rows(
    rows: list[MeasurementRow],
    start: date,
    end: date,
    station_code: str | None = None,
) -> list[tuple[datetime, float]]:
    """Filter measurement rows by date range and optional station code."""
    results: list[tuple[datetime, float]] = []
    for row in rows:
        if not start <= row.timestamp.date() <= end:
            continue
        if station_code:
            val = row.values.get(station_code)
            if val is not None:
                results.append((row.timestamp, val))
        else:
            for val in row.values.values():
                if val is not None:
                    results.append((row.timestamp, val))
    return results


def _collect_matching_codes(
    args: argparse.Namespace,
    measurements_dir: Path,
    file_indicator: str,
) -> set[str]:
    """Collect station codes that have data for the given parameters."""
    grouped = group_measurement_files_by_key(measurements_dir)
    matching: set[str] = set()
    for key, fpath in grouped.items():
        if key.indicator != file_indicator or key.frequency != args.frequency:
            continue
        mf = parse_measurement_file(fpath)
        for row in mf.rows:
            if not args.start <= row.timestamp.date() <= args.end:
                continue
            matching.update(c for c, v in row.values.items() if v is not None)
    return matching


def cmd_random_station(args: argparse.Namespace) -> None:
    """Display a random station measuring the given indicator in the time range."""
    stations_path, measurements_dir = _resolve_paths(args)
    stations = parse_stations(stations_path)
    file_indicator = normalize_indicator(args.indicator)
    matching_codes = _collect_matching_codes(args, measurements_dir, file_indicator)

    if not matching_codes:
        logger.warning(
            "No measurements found for indicator=%s, frequency=%s in [%s, %s]",
            args.indicator,
            args.frequency,
            args.start,
            args.end,
        )
        return

    station_map = {s.code: s for s in stations}
    valid = [station_map[c] for c in matching_codes if c in station_map]

    if not valid:
        logger.warning("No stations matched the measurement codes.")
        return

    chosen = random.choice(valid)
    print(f"Station: {chosen.name}")
    print(
        f"Address: {chosen.address or '(no address)'}, {chosen.city}, {chosen.voivodeship}"
    )


def cmd_stats(args: argparse.Namespace) -> None:
    """Compute mean and standard deviation for a station."""
    _, measurements_dir = _resolve_paths(args)
    file_indicator = normalize_indicator(args.indicator)
    grouped = group_measurement_files_by_key(measurements_dir)

    values: list[float] = []
    found_any = False

    for key, fpath in grouped.items():
        if key.indicator != file_indicator or key.frequency != args.frequency:
            continue
        found_any = True
        mf = parse_measurement_file(fpath)
        filtered = filter_rows(mf.rows, args.start, args.end, station_code=args.station)
        values.extend(v for _, v in filtered)

    if not found_any:
        logger.warning(
            "No files found for indicator=%s, frequency=%s",
            args.indicator,
            args.frequency,
        )
        return

    if not values:
        logger.warning(
            "No measurements for station=%s, indicator=%s in [%s, %s]",
            args.station,
            args.indicator,
            args.start,
            args.end,
        )
        return

    mean = statistics.mean(values)
    stdev = statistics.stdev(values) if len(values) > 1 else 0.0
    print(f"Station: {args.station}")
    print(f"Indicator: {args.indicator} ({args.frequency})")
    print(f"Period: {args.start} — {args.end}")
    print(f"Count: {len(values)}")
    print(f"Mean: {mean:.4f}")
    print(f"Std dev: {stdev:.4f}")


def _collect_flat_measurements(
    args: argparse.Namespace,
    measurements_dir: Path,
    file_indicator: str,
) -> tuple[list[tuple[datetime, float | None, str, str]], bool]:
    """Collect flat measurement tuples for anomaly detection."""
    grouped = group_measurement_files_by_key(measurements_dir)
    flat: list[tuple[datetime, float | None, str, str]] = []
    found_any = False
    for key, fpath in grouped.items():
        if key.indicator != file_indicator or key.frequency != args.frequency:
            continue
        found_any = True
        mf = parse_measurement_file(fpath)
        for row in mf.rows:
            if not args.start <= row.timestamp.date() <= args.end:
                continue
            for code, val in row.values.items():
                flat.append((row.timestamp, val, code, args.indicator))
    return flat, found_any


def cmd_anomalies(args: argparse.Namespace) -> None:
    """Detect and display measurement anomalies."""
    _, measurements_dir = _resolve_paths(args)
    file_indicator = normalize_indicator(args.indicator)
    flat, found_any = _collect_flat_measurements(args, measurements_dir, file_indicator)

    if not found_any:
        logger.warning(
            "No files found for indicator=%s, frequency=%s",
            args.indicator,
            args.frequency,
        )
        return

    if not flat:
        logger.warning("No data in the given time range.")
        return

    found = detect_anomalies(flat)
    if not found:
        print("No anomalies detected.")
        return

    print(f"Detected {len(found)} anomalies:")
    for anomaly in found[:50]:
        print(
            f"  [{anomaly.timestamp}] {anomaly.station_code}: "
            f"{anomaly.reason} (value={anomaly.value})"
        )
    if len(found) > 50:
        print(f"  ... and {len(found) - 50} more")


def _print_regex_results(results: dict[str, object]) -> None:  # pylint: disable=too-many-locals
    """Pretty-print the results of all regex analyses."""
    dates = results["dates"]
    print(f"=== Dates (YYYY-MM-DD) — {len(dates)} found ===")
    for d in list(dates)[:10]:
        print(f"  {d}")

    coords = results["coordinates"]
    print(f"\n=== Coordinates — {len(coords)} found ===")
    for lat, lon in list(coords)[:10]:
        print(f"  {lat}, {lon}")

    hyph = results["hyphenated"]
    print(f"\n=== Hyphenated station names — {len(hyph)} found ===")
    for name in list(hyph)[:10]:
        print(f"  {name}")

    normed = results["normalized_names"]
    print("\n=== Normalized names (first 10) ===")
    for name in list(normed)[:10]:
        print(f"  {name}")

    mob = results["mob_verification"]
    print(f"\n=== MOB verification — {len(mob)} stations ===")
    mismatches = [(c, k) for c, k, ok in mob if not ok]
    if mismatches:
        for code, kind in mismatches:
            print(f"  MISMATCH: {code} has kind={kind!r}")
    else:
        print("  All MOB stations are 'mobilna'.")

    three = results["three_part"]
    print(f"\n=== Three-part locations — {len(three)} found ===")
    for name in list(three)[:10]:
        print(f"  {name}")

    streets = results["street_locations"]
    print(f"\n=== Locations with comma + ul./al. — {len(streets)} found ===")
    for addr in list(streets)[:10]:
        print(f"  {addr}")


def cmd_regex_analysis(args: argparse.Namespace) -> None:
    """Run all regex analyses on stacje.csv."""
    stations_path, _ = _resolve_paths(args)
    results = run_all_analyses(stations_path)
    _print_regex_results(results)


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        prog="air_quality",
        description="Air quality measurement analysis tool",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=".",
        help="Base directory containing stacje.csv and measurements/",
    )
    parser.add_argument(
        "--indicator",
        type=_valid_indicator,
        default="PM10",
        help="Measured quantity (e.g. PM10, PM25, NO2)",
    )
    parser.add_argument(
        "--frequency",
        type=_valid_frequency,
        default="1g",
        help="Measurement frequency (1g, 24g, 1m)",
    )
    parser.add_argument(
        "--start",
        type=_valid_date,
        default="2023-01-01",
        help="Start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end",
        type=_valid_date,
        default="2023-12-31",
        help="End date (YYYY-MM-DD)",
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")
    sub.add_parser("random-station", help="Show random station for given parameters")

    stats_p = sub.add_parser("stats", help="Compute mean and std dev for a station")
    stats_p.add_argument("station", type=str, help="Station code")

    sub.add_parser("anomalies", help="Detect measurement anomalies")
    sub.add_parser("regex-analysis", help="Run regex analyses on stacje.csv (task 4)")

    return parser


def main() -> None:
    """Entry point for the argparse CLI."""
    setup_logging()
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    commands = {
        "random-station": cmd_random_station,
        "stats": cmd_stats,
        "anomalies": cmd_anomalies,
        "regex-analysis": cmd_regex_analysis,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
