import uvicorn
from flask import Flask, Response, redirect, request, url_for
from icons import (
    ARROW_DOWN,
    ARROW_LEFT,
    ARROW_RIGHT_SM,
    ARROW_UP,
    BUS_ICON_SM,
    CHART_ICON,
    CLOCK_ICON,
    CLOCK_ICON_SM,
    LINES_ICON,
    LINES_ICON_SM,
    MAP_PIN,
    MOON_ICON_SM,
    NAV_ICON,
    NAV_ICON_SM,
    SEARCH_ICON,
    SEARCH_ICON_LG,
    SEARCH_ICON_SM,
    TRAM_ICON_SM,
)
from services import search_stops_preview, stop_statistics
from uvicorn.middleware.wsgi import WSGIMiddleware

TAILWIND_CONFIG = """
tailwind.config = {
    theme: {
        extend: {
            colors: {
                wroclaw: {
                    red: '#BA0C2F',
                    dark: '#7F1028',
                    yellow: '#FFC928',
                    cream: '#FFF7D6'
                }
            },
            fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
            boxShadow: {
                glow: '0 24px 80px rgba(186, 12, 47, 0.22)'
            }
        }
    }
}
"""

BASE_HEAD = """<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script>{config}</script>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-wroclaw-dark font-sans text-zinc-950 antialiased">
"""

INDEX_TEMPLATE = (
    BASE_HEAD
    + """  <div class="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top_left,#FFC928_0,#BA0C2F_34%,#7F1028_64%,#26040D_100%)]">
    <div class="pointer-events-none absolute -left-24 top-28 h-72 w-72 rounded-full bg-wroclaw-yellow/30 blur-3xl"></div>
    <div class="pointer-events-none absolute right-0 top-0 h-96 w-96 rounded-full bg-white/10 blur-3xl"></div>
    <div class="relative flex min-h-screen flex-col">
      <header class="px-4 py-5 sm:px-6 lg:px-8">
        <div class="mx-auto flex max-w-6xl items-center justify-between gap-4 rounded-[2rem] border border-white/15 bg-white/10 px-5 py-4 text-white shadow-glow backdrop-blur">
          <div class="flex items-center gap-4">
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-wroclaw-yellow text-wroclaw-dark shadow-lg shadow-black/20">{nav_icon}</div>
            <div>
              <p class="text-xs font-bold uppercase tracking-[0.28em] text-wroclaw-yellow">MPK Wrocław</p>
              <h1 class="text-xl font-black tracking-tight sm:text-2xl">Rozkład jazdy</h1>
            </div>
          </div>
          <div class="hidden rounded-full border border-wroclaw-yellow/40 bg-wroclaw-yellow/15 px-4 py-2 text-sm font-bold text-wroclaw-yellow sm:block">GTFS live browser</div>
        </div>
      </header>
      <main class="mx-auto flex w-full max-w-6xl flex-1 flex-col px-4 pb-10 pt-4 sm:px-6 lg:px-8">
        <section class="grid items-center gap-8 py-8 lg:grid-cols-[0.9fr_1.1fr] lg:py-14">
          <div class="text-white">
            <p class="mb-4 inline-flex rounded-full bg-wroclaw-yellow px-4 py-2 text-xs font-black uppercase tracking-[0.24em] text-wroclaw-dark shadow-lg shadow-black/20">Czerwono-żółty Wrocław</p>
            <h2 class="max-w-xl text-5xl font-black leading-[0.95] tracking-tight sm:text-6xl lg:text-7xl">Znajdź swój przystanek szybciej.</h2>
            <p class="mt-5 max-w-lg text-lg leading-8 text-white/75">Wyszukuj po nazwie, kodzie albo ID i sprawdzaj linie, kierunki oraz dzienną liczbę odjazdów.</p>
          </div>
          <form method="get" autocomplete="off" class="rounded-xl border border-zinc-200 bg-white p-2 shadow-lg shadow-black/10">
            <div class="grid gap-2 sm:grid-cols-[1fr_auto]">
              <label class="relative block">
                <span class="absolute left-4 top-1/2 -translate-y-1/2 text-wroclaw-red">{search_icon}</span>
                <input name="q" value="{query}" placeholder="Nazwa, kod lub ID przystanku" autofocus
                       class="h-12 w-full rounded-lg border border-zinc-300 bg-white pl-12 pr-4 text-base font-semibold text-wroclaw-dark placeholder-zinc-400 outline-none transition focus:border-wroclaw-red focus:ring-4 focus:ring-wroclaw-red/15">
              </label>
              <button type="submit" class="inline-flex h-12 items-center justify-center gap-2 rounded-lg border-2 border-white bg-[#5f0618] px-6 text-sm font-black uppercase tracking-wide text-white shadow-md shadow-black/20 ring-1 ring-[#5f0618] transition hover:bg-black active:scale-[0.99]">
                {search_icon_sm}
                Szukaj
              </button>
            </div>
          </form>
        </section>
{results_section}      </main>
      <footer class="px-4 pb-6 text-center text-xs font-semibold uppercase tracking-[0.18em] text-white/50 sm:px-6 lg:px-8">
        MPK Wrocław GTFS / <a href="https://github.com/kguzek/coursework-wust/tree/main/js/lab10" class="text-wroclaw-yellow underline decoration-wroclaw-yellow/40 underline-offset-4 hover:text-white">repozytorium</a>
      </footer>
    </div>
  </div>
</body>
</html>"""
)

STOP_CARD = """
        <article>
          <a href="{detail_url}" class="group block rounded-xl border border-zinc-200 bg-white p-4 text-inherit no-underline shadow-sm transition hover:-translate-y-0.5 hover:border-wroclaw-red/40 hover:shadow-lg hover:shadow-black/10">
            <div class="flex items-start justify-between gap-4">
              <div class="flex min-w-0 items-start gap-3">
                <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-wroclaw-red text-white shadow-sm">{pin_icon}</div>
                <div class="min-w-0">
                  <h3 class="truncate text-base font-semibold leading-tight text-zinc-950">{name}</h3>
                  <div class="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-zinc-500">
                    <span>Kod <span class="font-medium text-zinc-900">{code}</span></span>
                    {location}
                  </div>
                </div>
              </div>
              <div class="flex shrink-0 flex-wrap justify-end gap-1.5">{badges}</div>
            </div>
            <div class="mt-3 flex flex-col gap-3 rounded-lg bg-zinc-50 p-3 sm:flex-row sm:items-center sm:justify-between">
              <div class="flex flex-wrap gap-2">{stats}</div>
              <span class="inline-flex shrink-0 items-center justify-center gap-1.5 self-start rounded-md bg-wroclaw-red px-3 py-1.5 text-sm font-semibold text-white shadow-sm transition group-hover:bg-wroclaw-dark sm:self-auto">
                Zobacz szczegóły {arrow_icon}
              </span>
            </div>
          </a>
        </article>
"""


def _badge(n: int, icon: str, variant: str) -> str:
    return f'<span class="inline-flex items-center gap-1 rounded-md px-2 py-1 text-xs font-medium {variant}">{icon} {n}</span>'


def _build_badges(preview: dict) -> str:
    parts = []
    if preview["bus_lines"]:
        parts.append(
            _badge(preview["bus_lines"], BUS_ICON_SM, "bg-wroclaw-red text-white")
        )
    if preview["tram_lines"]:
        parts.append(
            _badge(
                preview["tram_lines"],
                TRAM_ICON_SM,
                "bg-wroclaw-yellow text-wroclaw-dark",
            )
        )
    if preview["night_lines"]:
        parts.append(
            _badge(
                preview["night_lines"],
                MOON_ICON_SM,
                "bg-wroclaw-dark text-wroclaw-yellow",
            )
        )
    return "\n".join(parts)


def _location_line(lat: object, lon: object) -> str:
    pin = (
        '<svg class="inline h-3 w-3 -mt-0.5" fill="none" stroke="currentColor" '
        'viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" '
        'stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0'
        'l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" '
        'stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>'
    )
    return f'<span class="text-zinc-500">{pin} {float(lat):.4f}, {float(lon):.4f}</span>'


def _build_stats(preview: dict) -> str:
    return "\n".join(
        [
        f'<span class="inline-flex items-center gap-1.5 rounded-md bg-zinc-100 px-2 py-1 text-sm font-medium text-zinc-700">{LINES_ICON_SM}<span><strong class="text-zinc-950">{preview["lines"]}</strong> linii</span></span>',
        f'<span class="inline-flex items-center gap-1.5 rounded-md bg-zinc-100 px-2 py-1 text-sm font-medium text-zinc-700">{CLOCK_ICON_SM}<span><strong class="text-zinc-950">{preview["departures"]}</strong> odjazdów</span></span>',
        ]
    )


def _preview_html(stops: list) -> str:
    cards = "\n".join(
        STOP_CARD.format(
            detail_url=url_for("stop_page", stop_id=stop["stop_id"]),
            pin_icon=MAP_PIN,
            name=stop["stop_name"],
            code=stop["stop_code"],
            location=_location_line(stop["stop_lat"], stop["stop_lon"]),
            badges=_build_badges(stop),
            stats=_build_stats(stop),
            arrow_icon=ARROW_RIGHT_SM,
        )
        for stop in stops
    )
    header = (
        f'<div class="mb-5 flex items-center justify-between rounded-[1.5rem] border border-white/20 bg-white/15 px-5 py-4 text-white backdrop-blur">'
        f'<h2 class="flex items-center gap-2 text-lg font-black">'
        f'{LINES_ICON} Wyniki <span class="font-semibold text-wroclaw-yellow">({len(stops)} przystanków)</span></h2></div>'
    )
    return f'{header}<div class="grid gap-2.5">{cards}</div>\n'


EMPTY_STATE = f"""
      <div class="rounded-[2rem] border border-white/20 bg-white/10 px-6 py-16 text-center text-white shadow-glow backdrop-blur">
        <div class="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-wroclaw-yellow text-wroclaw-dark shadow-xl shadow-black/20">{SEARCH_ICON_LG}</div>
        <h2 class="text-2xl font-black">Znajdź przystanek</h2>
        <p class="mt-2 text-white/65">Szukaj po nazwie, kodzie lub numerze ID</p>
      </div>"""

NO_RESULTS = f"""
      <div class="rounded-[2rem] border border-wroclaw-yellow/40 bg-white px-6 py-16 text-center shadow-glow">
        <div class="mx-auto mb-5 flex h-20 w-20 items-center justify-center rounded-3xl bg-wroclaw-red text-wroclaw-yellow shadow-xl shadow-wroclaw-red/25">{SEARCH_ICON_LG}</div>
        <h2 class="text-2xl font-black text-wroclaw-dark">Nie znaleziono przystanków</h2>
        <p class="mt-2 font-semibold text-zinc-500">Spróbuj innego zapytania</p>
      </div>"""

STOP_DETAIL_TEMPLATE = (
    BASE_HEAD
    + """
  <div class="relative min-h-screen overflow-hidden bg-[radial-gradient(circle_at_top_right,#FFC928_0,#BA0C2F_38%,#7F1028_68%,#26040D_100%)]">
    <div class="pointer-events-none absolute -right-20 top-20 h-80 w-80 rounded-full bg-wroclaw-yellow/30 blur-3xl"></div>
    <div class="relative flex min-h-screen flex-col">
      <header class="px-4 py-5 sm:px-6 lg:px-8">
        <div class="mx-auto flex max-w-6xl items-center gap-4 rounded-[2rem] border border-white/15 bg-white/10 px-5 py-4 text-white shadow-glow backdrop-blur">
          <a href="/" class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-wroclaw-yellow text-wroclaw-dark shadow-lg shadow-black/20 transition hover:-translate-x-1">{arrow_left}</a>
          <div class="min-w-0">
            <p class="text-xs font-bold uppercase tracking-[0.28em] text-wroclaw-yellow">Przystanek</p>
            <h1 class="truncate text-xl font-black tracking-tight sm:text-2xl">{stop_name}</h1>
            <p class="text-sm font-semibold text-white/70">Kod: {stop_code} / ID: {stop_id}</p>
          </div>
        </div>
      </header>
      <main class="mx-auto w-full max-w-6xl flex-1 space-y-6 px-4 py-6 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">{stat_cards}</div>
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">{detail_sections}</div>
      </main>
      <footer class="px-4 pb-6 text-center text-xs font-semibold uppercase tracking-[0.18em] text-white/50 sm:px-6 lg:px-8">
        MPK Wrocław GTFS / <a href="/" class="text-wroclaw-yellow underline decoration-wroclaw-yellow/40 underline-offset-4 hover:text-white">powrót do wyszukiwarki</a> / <a href="https://github.com/kguzek/coursework-wust/tree/main/js/lab10" class="text-wroclaw-yellow underline decoration-wroclaw-yellow/40 underline-offset-4 hover:text-white">repozytorium</a>
      </footer>
    </div>
  </div>
</body>
</html>"""
)


def _stat_card(value: str, label: str, icon: str, accent: str) -> str:
    return f"""
          <div class="flex items-center gap-4 rounded-[1.75rem] border border-wroclaw-yellow/30 bg-white p-5 shadow-2xl shadow-black/10">
            <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl shadow-lg shadow-black/10 {accent}">{icon}</div>
            <div>
              <div class="text-2xl font-black tracking-tight text-wroclaw-dark">{value}</div>
              <div class="mt-0.5 text-xs font-bold uppercase tracking-wide text-zinc-500">{label}</div>
            </div>
          </div>"""


def _direction_table(directions: list) -> str:
    if not directions:
        return """<div class="rounded-[1.75rem] bg-white p-8 text-center text-sm font-semibold text-zinc-400">Brak danych o kierunkach</div>"""
    badge = (
        "inline-flex h-8 min-w-[2.75rem] items-center justify-center rounded-full "
        "bg-wroclaw-red px-3 text-sm font-black text-white"
    )
    rows = "".join(
        f"""
            <tr class="border-b border-wroclaw-yellow/20 transition hover:bg-wroclaw-cream/60">
              <td class="px-4 py-3">
                <div class="flex items-center gap-2">
                  <span class="flex h-8 w-8 items-center justify-center rounded-xl bg-wroclaw-yellow text-wroclaw-dark">{NAV_ICON_SM}</span>
                  <span class="font-bold text-wroclaw-dark">{d["trip_headsign"]}</span>
                </div>
              </td>
              <td class="px-4 py-3 text-right">
                <span class="{badge}">{d["departures"]}</span>
              </td>
            </tr>"""
        for d in directions
    )
    return f"""
          <div class="overflow-hidden rounded-[1.75rem] border border-wroclaw-yellow/30 bg-white shadow-2xl shadow-black/10">
            <div class="flex items-center gap-2 border-b border-wroclaw-yellow/30 bg-wroclaw-cream px-5 py-4 text-sm font-black uppercase tracking-wide text-wroclaw-dark">{NAV_ICON} Najczęstsze kierunki</div>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead><tr class="text-xs uppercase tracking-wider text-zinc-400">
                  <th class="px-4 py-3 text-left font-black">Kierunek</th>
                  <th class="px-4 py-3 text-right font-black">Odjazdy</th>
                </tr></thead>
                <tbody>{rows}</tbody>
              </table>
            </div>
          </div>"""


def route_row(r: dict) -> str:
    bg = (
        "bg-wroclaw-red text-white"
        if r["route_type"] == 30
        else "bg-wroclaw-yellow text-wroclaw-dark"
    )
    icon = BUS_ICON_SM if r["route_type"] == 30 else TRAM_ICON_SM
    badge_cls = (
        "inline-flex h-8 min-w-[2.75rem] items-center justify-center rounded-full "
        "bg-wroclaw-dark px-3 text-sm font-black text-wroclaw-yellow"
    )
    return f"""
            <tr class="border-b border-wroclaw-yellow/20 transition hover:bg-wroclaw-cream/60">
              <td class="px-4 py-3">
                <div class="flex items-center gap-2">
                  <span class="flex h-8 w-8 items-center justify-center rounded-xl {bg}">{icon}</span>
                  <span class="font-black text-wroclaw-dark">{r["route_short_name"]}</span>
                </div>
              </td>
              <td class="px-4 py-3 text-right">
                <span class="{badge_cls}">{r["departures"]}</span>
              </td>
            </tr>"""


def _route_table(routes: list, avg: str) -> str:
    if not routes:
        return """<div class="rounded-[1.75rem] bg-white p-8 text-center text-sm font-semibold text-zinc-400">Brak danych o liniach</div>"""
    rows = "".join(route_row(r) for r in routes)
    return f"""
          <div class="overflow-hidden rounded-[1.75rem] border border-wroclaw-yellow/30 bg-white shadow-2xl shadow-black/10">
            <div class="flex items-center gap-2 border-b border-wroclaw-yellow/30 bg-wroclaw-cream px-5 py-4 text-sm font-black uppercase tracking-wide text-wroclaw-dark">
              {CHART_ICON} Najbardziej obciążone linie
              <span class="ml-auto rounded-full bg-wroclaw-yellow px-3 py-1 text-xs font-black normal-case tracking-normal text-wroclaw-dark">śr. {avg}/linię</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead><tr class="text-xs uppercase tracking-wider text-zinc-400">
                  <th class="px-4 py-3 text-left font-black">Linia</th>
                  <th class="px-4 py-3 text-right font-black">Odjazdy</th>
                </tr></thead>
                <tbody>{rows}</tbody>
              </table>
            </div>
          </div>"""


def create_app(database: str | None = None) -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index() -> str:
        query = request.args.get("q", "").strip()
        if query:
            stops = search_stops_preview(query, database)
            results = _preview_html(stops) if stops else NO_RESULTS
        else:
            results = EMPTY_STATE

        return INDEX_TEMPLATE.format(
            title="Rozkład jazdy Wrocław",
            config=TAILWIND_CONFIG,
            search_icon=SEARCH_ICON,
            search_icon_sm=SEARCH_ICON_SM,
            query=query,
            results_section=results,
            nav_icon=NAV_ICON,
        )

    @app.get("/stops/<int:stop_id>")
    def stop_page(stop_id: int) -> str | Response:
        try:
            stats = stop_statistics(stop_id, database)
        except ValueError:
            return redirect(url_for("index"))

        s = stats["stop"]
        avg = (
            f"{stats['average_departures_per_line']:.1f}"
            if stats["average_departures_per_line"]
            else "n/a"
        )
        earliest = stats["earliest_departure"] or "\u2014"
        latest = stats["latest_departure"] or "\u2014"

        stat_cards = "".join(
            [
                _stat_card(
                    str(stats["distinct_lines"]),
                    "Linie",
                    LINES_ICON,
                    "bg-wroclaw-yellow text-wroclaw-dark",
                ),
                _stat_card(
                    str(stats["departures"]),
                    "Odjazdy dziennie",
                    CLOCK_ICON,
                    "bg-wroclaw-red text-white",
                ),
                _stat_card(
                    earliest,
                    "Pierwszy odjazd",
                    ARROW_UP,
                    "bg-wroclaw-cream text-wroclaw-red",
                ),
                _stat_card(
                    latest,
                    "Ostatni odjazd",
                    ARROW_DOWN,
                    "bg-wroclaw-dark text-wroclaw-yellow",
                ),
            ]
        )

        detail_sections = "".join(
            [
                _direction_table(stats["common_directions"]),
                _route_table(stats["busiest_routes"], avg),
            ]
        )

        return STOP_DETAIL_TEMPLATE.format(
            title=f"{s['stop_name']} \u2014 Rozkład jazdy Wrocław",
            config=TAILWIND_CONFIG,
            stop_name=s["stop_name"],
            stop_code=s["stop_code"],
            stop_id=s["stop_id"],
            arrow_left=ARROW_LEFT,
            stat_cards=stat_cards,
            detail_sections=detail_sections,
        )

    return app


def main() -> None:
    uvicorn.run(WSGIMiddleware(create_app()), host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
