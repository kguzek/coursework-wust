# pylint: disable=too-few-public-methods
from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Agency(Base):
    __tablename__ = "agency"

    agency_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agency_name: Mapped[str] = mapped_column(Text)
    agency_url: Mapped[str] = mapped_column(Text)
    agency_timezone: Mapped[str] = mapped_column(Text)
    agency_phone: Mapped[str | None] = mapped_column(Text)
    agency_lang: Mapped[str | None] = mapped_column(Text)
    routes: Mapped[list["Route"]] = relationship(back_populates="agency")


class RouteType(Base):
    __tablename__ = "route_types"

    route_type2_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    route_type2_name: Mapped[str] = mapped_column(Text)
    routes: Mapped[list["Route"]] = relationship(back_populates="route_type2")


class VehicleType(Base):
    __tablename__ = "vehicle_types"

    vehicle_type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_type_name: Mapped[str] = mapped_column(Text)
    vehicle_type_description: Mapped[str | None] = mapped_column(Text)
    vehicle_type_symbol: Mapped[str | None] = mapped_column(Text)
    trips: Mapped[list["Trip"]] = relationship(back_populates="vehicle")


class Calendar(Base):
    __tablename__ = "calendar"

    service_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    monday: Mapped[bool] = mapped_column(Boolean)
    tuesday: Mapped[bool] = mapped_column(Boolean)
    wednesday: Mapped[bool] = mapped_column(Boolean)
    thursday: Mapped[bool] = mapped_column(Boolean)
    friday: Mapped[bool] = mapped_column(Boolean)
    saturday: Mapped[bool] = mapped_column(Boolean)
    sunday: Mapped[bool] = mapped_column(Boolean)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    trips: Mapped[list["Trip"]] = relationship(back_populates="calendar")


class Stop(Base):
    __tablename__ = "stops"

    stop_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stop_code: Mapped[str] = mapped_column(Text)
    stop_name: Mapped[str] = mapped_column(Text)
    stop_lat: Mapped[Decimal] = mapped_column(Numeric(12, 10))
    stop_lon: Mapped[Decimal] = mapped_column(Numeric(13, 10))
    stop_times: Mapped[list["StopTime"]] = relationship(back_populates="stop")


class Route(Base):
    __tablename__ = "routes"

    route_id: Mapped[str] = mapped_column(String, primary_key=True)
    agency_id: Mapped[int] = mapped_column(ForeignKey("agency.agency_id"))
    route_short_name: Mapped[str] = mapped_column(Text)
    route_long_name: Mapped[str | None] = mapped_column(Text)
    route_desc: Mapped[str] = mapped_column(Text)
    route_type: Mapped[int] = mapped_column(Integer)
    route_type2_id: Mapped[int | None] = mapped_column(ForeignKey("route_types.route_type2_id"))
    valid_from: Mapped[date] = mapped_column(Date)
    valid_until: Mapped[date] = mapped_column(Date)
    agency: Mapped[Agency] = relationship(back_populates="routes")
    route_type2: Mapped[RouteType | None] = relationship(back_populates="routes")
    trips: Mapped[list["Trip"]] = relationship(back_populates="route")


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[str] = mapped_column(String, primary_key=True)
    route_id: Mapped[str] = mapped_column(ForeignKey("routes.route_id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("calendar.service_id"))
    trip_headsign: Mapped[str] = mapped_column(Text)
    direction_id: Mapped[int] = mapped_column(Integer)
    shape_id: Mapped[int | None] = mapped_column(Integer)
    brigade_id: Mapped[int | None] = mapped_column(Integer)
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicle_types.vehicle_type_id"))
    variant_id: Mapped[int | None] = mapped_column(Integer)
    route: Mapped[Route] = relationship(back_populates="trips")
    calendar: Mapped[Calendar] = relationship(back_populates="trips")
    vehicle: Mapped[VehicleType | None] = relationship(back_populates="trips")
    stop_times: Mapped[list["StopTime"]] = relationship(back_populates="trip")


class StopTime(Base):
    __tablename__ = "stop_times"

    trip_id: Mapped[str] = mapped_column(ForeignKey("trips.trip_id"), primary_key=True)
    stop_sequence: Mapped[int] = mapped_column(Integer, primary_key=True)
    arrival_time: Mapped[str] = mapped_column(Text)
    arrival_seconds: Mapped[int] = mapped_column(Integer)
    departure_time: Mapped[str] = mapped_column(Text)
    departure_seconds: Mapped[int] = mapped_column(Integer)
    stop_id: Mapped[int] = mapped_column(ForeignKey("stops.stop_id"))
    pickup_type: Mapped[int | None] = mapped_column(Integer)
    drop_off_type: Mapped[int | None] = mapped_column(Integer)
    trip: Mapped[Trip] = relationship(back_populates="stop_times")
    stop: Mapped[Stop] = relationship(back_populates="stop_times")


MODEL_BY_TABLE = {
    "agency": Agency,
    "route_types": RouteType,
    "vehicle_types": VehicleType,
    "calendar": Calendar,
    "stops": Stop,
    "routes": Route,
    "trips": Trip,
    "stop_times": StopTime,
}
