import csv
from pathlib import Path
from typing import Any, Self


class Station:
    def __init__(
        self,
        nr: int,
        station_code: str,
        international_code: str,
        name: str,
        old_code: str,
        start_date: str,
        end_date: str,
        station_type: str,
        area_type: str,
        station_kind: str,
        voivodeship: str,
        city: str,
        address: str,
        lat: float | None,
        lon: float | None,
    ) -> None:
        self.nr = nr
        self.station_code = station_code
        self.international_code = international_code
        self.name = name
        self.old_code = old_code
        self.start_date = start_date
        self.end_date = end_date
        self.station_type = station_type
        self.area_type = area_type
        self.station_kind = station_kind
        self.voivodeship = voivodeship
        self.city = city
        self.address = address
        self.lat = lat
        self.lon = lon

    def __str__(self) -> str:
        return f"Station({self.station_code}, {self.name}, {self.city})"

    def __repr__(self) -> str:
        return f"Station(code={self.station_code!r}, name={self.name!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Station) and self.station_code == other.station_code

    def __hash__(self) -> int:
        return hash(self.station_code)

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Self:
        def to_float(value: Any) -> float | None:
            text = str(value).replace(",", ".").strip()
            if not text:
                return None
            try:
                return float(text)
            except ValueError:
                return None

        old_code_key = next((key for key in row if "Stary Kod" in key), "")
        return cls(
            nr=int(row.get("Nr", 0) or 0),
            station_code=str(row.get("Kod stacji", "")).strip(),
            international_code=str(row.get("Kod międzynarodowy", "")).strip(),
            name=str(row.get("Nazwa stacji", "")).strip(),
            old_code=str(row.get(old_code_key, "")).strip(),
            start_date=str(row.get("Data uruchomienia", "")).strip(),
            end_date=str(row.get("Data zamknięcia", "")).strip(),
            station_type=str(row.get("Typ stacji", "")).strip(),
            area_type=str(row.get("Typ obszaru", "")).strip(),
            station_kind=str(row.get("Rodzaj stacji", "")).strip(),
            voivodeship=str(row.get("Województwo", "")).strip(),
            city=str(row.get("Miejscowość", "")).strip(),
            address=str(row.get("Adres", "")).strip(),
            lat=to_float(row.get("WGS84 φ N", "")),
            lon=to_float(row.get("WGS84 λ E", "")),
        )


def load_stations(csv_path: str | Path) -> dict[str, Station]:
    stations: dict[str, Station] = {}
    with open(csv_path, encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            station = Station.from_row(row)
            if station.station_code:
                stations[station.station_code] = station
    return stations
