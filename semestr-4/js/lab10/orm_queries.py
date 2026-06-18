from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from orm_loader import orm_engine
from orm_models import Route, StopTime, Trip


def route_departure_counts(stop_id: int, database: str | None = None) -> list[tuple[str, int]]:
    statement = (
        select(Route.route_short_name, func.count(StopTime.trip_id).label("departures"))  # pylint: disable=not-callable
        .join(Trip, Trip.route_id == Route.route_id)
        .join(StopTime, StopTime.trip_id == Trip.trip_id)
        .where(StopTime.stop_id == stop_id)
        .group_by(Route.route_short_name)
        .order_by(desc("departures"), Route.route_short_name)
        .limit(10)
    )
    with Session(orm_engine(database)) as session:
        return list(session.execute(statement))
