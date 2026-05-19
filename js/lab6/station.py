import csv
from pathlib import Path

# pylint: disable-all


class Station:
    def __init__(
        self,
        nr,
        station_code,
        international_code,
        name,
        old_code,
        start_date,
        end_date,
        station_type,
        area_type,
        station_kind,
        voivodeship,
        city,
        address,
        lat,
        lon,
    ):
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

    def __str__(self):
        return f"Station({self.station_code}, {self.name}, {self.city})"

    def __repr__(self):
        return f"Station(code={self.station_code!r}, name={self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, Station):
            return NotImplemented
        return self.station_code == other.station_code

    def __hash__(self):
        return hash(self.station_code)

    @classmethod
    def from_row(cls, row: dict) -> "Station":
        def to_float(v):
            try:
                return float(str(v).replace(",", ".")) if str(v).strip() else None
            except ValueError:
                return None

        old_code_key = next((k for k in row if "Stary Kod" in k), "")
        return cls(
            nr=int(row.get("Nr", 0) or 0),
            station_code=row.get("Kod stacji", "").strip(),
            international_code=row.get("Kod międzynarodowy", "").strip(),
            name=row.get("Nazwa stacji", "").strip(),
            old_code=row.get(old_code_key, "").strip(),
            start_date=row.get("Data uruchomienia", "").strip(),
            end_date=row.get("Data zamknięcia", "").strip(),
            station_type=row.get("Typ stacji", "").strip(),
            area_type=row.get("Typ obszaru", "").strip(),
            station_kind=row.get("Rodzaj stacji", "").strip(),
            voivodeship=row.get("Województwo", "").strip(),
            city=row.get("Miejscowość", "").strip(),
            address=row.get("Adres", "").strip(),
            lat=to_float(row.get("WGS84 φ N", "")),
            lon=to_float(row.get("WGS84 λ E", "")),
        )


def load_stations(csv_path: str | Path) -> dict[str, Station]:
    stations: dict[str, Station] = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            s = Station.from_row(row)
            if s.station_code:
                stations[s.station_code] = s
    return stations
