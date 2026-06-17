from flask import Flask, Response, redirect, render_template_string, request, url_for

from lab10.services import search_stops, stop_statistics


INDEX_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Wroclaw timetable</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }
    input, button { font: inherit; padding: .55rem .7rem; }
    input { min-width: min(32rem, 70vw); }
    table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
    th, td { border-bottom: 1px solid #ddd; padding: .55rem; text-align: left; }
    a { color: #0645ad; }
  </style>
</head>
<body>
  <h1>Wroclaw timetable</h1>
  <form method="get">
    <input name="q" value="{{ query }}" placeholder="Stop name, code, or id" autofocus>
    <button type="submit">Search</button>
  </form>
  {% if stops %}
    <table>
      <thead><tr><th>Stop</th><th>Code</th><th></th></tr></thead>
      <tbody>
      {% for stop in stops %}
        <tr>
          <td>{{ stop.stop_name }}</td>
          <td>{{ stop.stop_code }}</td>
          <td><a href="{{ url_for('stop_page', stop_id=stop.stop_id) }}">statistics</a></td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
  {% endif %}
</body>
</html>
"""

STOP_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ stats.stop.stop_name }}</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th, td { border-bottom: 1px solid #ddd; padding: .55rem; text-align: left; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr)); gap: 1rem; }
    .card { border: 1px solid #ddd; border-radius: .7rem; padding: 1rem; }
    .value { font-size: 1.6rem; font-weight: 700; }
  </style>
</head>
<body>
  <a href="{{ url_for('index') }}">Back</a>
  <h1>{{ stats.stop.stop_name }} <small>({{ stats.stop.stop_code }})</small></h1>
  <section class="cards">
    <div class="card"><div>Lines</div><div class="value">{{ stats.distinct_lines }}</div></div>
    <div class="card"><div>Departures</div><div class="value">{{ stats.departures }}</div></div>
    <div class="card"><div>First</div><div class="value">{{ stats.earliest_departure }}</div></div>
    <div class="card"><div>Last</div><div class="value">{{ stats.latest_departure }}</div></div>
  </section>
  <h2>Most common directions</h2>
  <table>
    {% for item in stats.common_directions %}
      <tr><td>{{ item.trip_headsign }}</td><td>{{ item.departures }}</td></tr>
    {% endfor %}
  </table>
  <h2>Busiest routes</h2>
  <table>
    {% for item in stats.busiest_routes %}
      <tr><td>{{ item.route_short_name }}</td><td>{{ item.departures }}</td></tr>
    {% endfor %}
  </table>
  <p>Average departures per line: {{ '%.2f'|format(stats.average_departures_per_line or 0) }}</p>
</body>
</html>
"""


def create_app(database: str | None = None) -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        query = request.args.get("q", "").strip()
        stops = search_stops(query, database) if query else []
        return render_template_string(INDEX_TEMPLATE, query=query, stops=stops)

    @app.get("/stops/<int:stop_id>")
    def stop_page(stop_id: int) -> str | Response:
        try:
            stats = stop_statistics(stop_id, database)
        except ValueError:
            return redirect(url_for("index"))
        return render_template_string(STOP_TEMPLATE, stats=stats)

    return app


def main() -> None:
    create_app().run(host="0.0.0.0", port=8000, debug=False)


if __name__ == "__main__":
    main()
