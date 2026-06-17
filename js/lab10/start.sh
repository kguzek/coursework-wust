#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

docker compose -f compose.yaml up -d

until docker compose -f compose.yaml exec -T postgres pg_isready -U lab10 -d lab10 >/dev/null 2>&1; do
  sleep 1
done

export LAB10_DATABASE_URL="${LAB10_DATABASE_URL:-postgresql://lab10:lab10@localhost:55432/lab10}"

python create_database.py
python load_data.py OtwartyWroclaw_rozklad_jazdy_GTFS_28052026.zip
python app.py
