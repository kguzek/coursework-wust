from typing import List

from tabulate import tabulate

from lab3.simulation import run_all_simulations, SimulationResult


def print_results(results: List[SimulationResult]):
    headers = ["Algorithm", "Page Faults", "Page Hits", "Requests", "Memory", "Pages"]
    table = [
        [
            r.algorithm,
            r.page_faults,
            r.page_hits,
            r.requests,
            r.memory,
            r.pages
        ]
        for r in results
    ]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def main() -> None:
    results = run_all_simulations()
    print_results(results)


if __name__ == "__main__":
    main()
