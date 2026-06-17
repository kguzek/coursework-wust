import argparse
from collections.abc import Sequence
from decimal import Decimal

from lab10.loader import create_database, load_gtfs
from lab10.orm_loader import create_database_orm, load_gtfs_orm
from lab10.orm_queries import route_departure_counts
from lab10.services import StopStats, search_stops, stop_statistics


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.handler(args)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lab10")
    subcommands = parser.add_subparsers(required=True)

    create_parser = subcommands.add_parser("create")
    create_parser.add_argument("database", nargs="?")
    create_parser.set_defaults(handler=handle_create)

    load_parser = subcommands.add_parser("load")
    load_parser.add_argument("source")
    load_parser.add_argument("database", nargs="?")
    load_parser.set_defaults(handler=handle_load)

    query_parser = subcommands.add_parser("query")
    query_parser.add_argument("database", nargs="?")
    query_parser.set_defaults(handler=handle_query)

    orm_create_parser = subcommands.add_parser("create-orm")
    orm_create_parser.add_argument("database", nargs="?")
    orm_create_parser.set_defaults(handler=handle_create_orm)

    orm_load_parser = subcommands.add_parser("load-orm")
    orm_load_parser.add_argument("source")
    orm_load_parser.add_argument("database", nargs="?")
    orm_load_parser.set_defaults(handler=handle_load_orm)

    orm_stats_parser = subcommands.add_parser("orm-stats")
    orm_stats_parser.add_argument("stop_id", type=int)
    orm_stats_parser.add_argument("database", nargs="?")
    orm_stats_parser.set_defaults(handler=handle_orm_stats)

    return parser


def handle_create(args: argparse.Namespace) -> None:
    create_database(args.database)


def handle_load(args: argparse.Namespace) -> None:
    load_gtfs(args.source, args.database)


def handle_create_orm(args: argparse.Namespace) -> None:
    create_database_orm(args.database)


def handle_load_orm(args: argparse.Namespace) -> None:
    load_gtfs_orm(args.source, args.database)


def handle_orm_stats(args: argparse.Namespace) -> None:
    for route_name, departures in route_departure_counts(args.stop_id, args.database):
        print(f"{route_name}: {departures}")


def handle_query(args: argparse.Namespace) -> None:
    query = input("Stop name/code/id: ").strip()
    choices = search_stops(query, args.database)
    if not choices:
        print("No stops found")
        return
    for index, stop in enumerate(choices, start=1):
        print(f"{index}. [{stop['stop_id']}] {stop['stop_name']} ({stop['stop_code']})")
    selected = int(input("Choose stop number: ").strip())
    stats = stop_statistics(choices[selected - 1]["stop_id"], args.database)
    print_stats(stats)


def print_stats(stats: StopStats) -> None:
    average = format_decimal(stats["average_departures_per_line"])
    print(f"Stop: {stats['stop']['stop_name']} ({stats['stop']['stop_code']})")
    print(f"Distinct lines: {stats['distinct_lines']}")
    print(f"Departures: {stats['departures']}")
    print(f"First departure: {stats['earliest_departure']}")
    print(f"Last departure: {stats['latest_departure']}")
    print("Most common directions:")
    for direction in stats["common_directions"]:
        print(f"  {direction['trip_headsign']}: {direction['departures']}")
    print("Busiest routes:")
    for route in stats["busiest_routes"]:
        print(f"  {route['route_short_name']}: {route['departures']}")
    print(f"Average departures per line: {average}")


def format_decimal(value: Decimal | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


if __name__ == "__main__":
    raise SystemExit(main())
