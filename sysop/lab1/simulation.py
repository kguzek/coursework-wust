"""Simulation module for the CPU scheduling algorithms."""
import functools
import random
import timeit
from concurrent.futures import as_completed, ProcessPoolExecutor
from typing import Callable

import matplotlib
from matplotlib import pyplot as plt
from tabulate import tabulate

from lab1.algorithms.fcfs import FCFS
from lab1.algorithms.rr import RR
from lab1.algorithms.sjf import SJF
from lab1.algorithms.srtf import SRTF
from lab1.common import generate_processes, SimulationResult, TestCase, DEFAULT_ITERATION_COUNT, DEBUG_MODE

try:
    # This will need an installation of
    # source sysop/.venv/bin/activate
    # pip install PyQt5
    matplotlib.use("Qt5Agg")
except ImportError:
    print("[warn] failed to use Qt5Agg backend. If this is a graphical environment, please run: pip install PyQt5")
TIME_QUANTUM = 2
MAX_SUMMARY_TEST_DESCRIPTIONS = 3


def run_simulation(process_count: int, average_arrival_time: float | None = None,
                   max_burst_time: int | None = None, *, n: int = None) -> dict[str, SimulationResult]:
    """Run the simulation for all algorithms with the given number of processes.
    :return: The run results for each algorithm, formatted as: average_completion_time, execution_log, starved_processes, processes."""

    processes = generate_processes(process_count,
                                   process_count ** 1.5 if average_arrival_time is None else average_arrival_time,
                                   process_count * 4 if max_burst_time is None else max_burst_time)

    algorithms = {
        "first come first serve": FCFS(processes),
        "shortest job first": SJF(processes),
        "shortest remaining time first": SRTF(processes),
        "round robin": RR(processes, TIME_QUANTUM),
    }

    results: dict[str, SimulationResult] = {}

    with ProcessPoolExecutor() as executor:
        future_to_algorithm = {
            executor.submit(algorithm.run): name
            for name, algorithm in algorithms.items()
        }

        for future in as_completed(future_to_algorithm):
            algorithm_name = future_to_algorithm[future]
            results[algorithm_name] = future.result()

    if DEBUG_MODE and n is not None:
        print(f"Iteration {n} complete")
    return dict(sorted(results.items(), key=lambda item: item[1][0]))


def get_average_result(results: list[SimulationResult]):
    """Get the average result from a list of results. Uses the last result to get the execution log and process list."""
    last_result = results[-1]
    average_completion_time = sum(result[0] for result in results) / len(results)
    execution_log = last_result[1]
    starved_processes = sum(result[2] for result in results) / len(results)
    processes = last_result[3]
    process_switches = sum(result[4] for result in results) / len(results)
    return average_completion_time, execution_log, starved_processes, processes, process_switches


def repeat_simulation(iterations: int, process_count: int, average_arrival_time: int | None = None,
                      max_burst_time: int = None, _=None) -> dict[str, SimulationResult]:
    all_results: dict[str, list[SimulationResult]] = {}

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(run_simulation, process_count, average_arrival_time, max_burst_time, n=n) for n in
            range(1, iterations + 1)
        ]

        for future in as_completed(futures):
            for algorithm, result in future.result().items():
                all_results.setdefault(algorithm, [])
                all_results[algorithm].append(result)

    average_results = {algorithm: get_average_result(results) for algorithm, results in all_results.items()}

    return average_results


def get_best_result(results: dict[str, SimulationResult]):
    """Get the best result from the results, according to the average completion time."""
    return min(results.items(), key=lambda i: i[1][0])


def present_results_cli(results: dict[str, SimulationResult], execution_time: float,
                        test_case_meta: tuple[int, TestCase] = None):
    """Present the results in the command line interface.

    :return: The best result in terms of average completion time."""

    headers = ["Algorithm", "Average Wait Time", "Average Idle Time", "Average Completion Time", "Process Switches",
               "Starved Processes", "Total Processes", "Time Taken",
               ]
    rows = [
        [algorithm.capitalize(), round(average_wait_time, 3),
         round(sum(process.get_idle_time() for process in processes) / len(processes), 3),
         round(sum(process.get_completion_time() for process in processes) / len(processes), 3),
         round(process_switches, 1), round(starved_processes, 1), len(processes),
         execution_log[-1][1]] for
        algorithm, (average_wait_time, execution_log, starved_processes, processes, process_switches) in
        results.items()
    ]
    best_result = get_best_result(results)[0]
    print()
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    if test_case_meta is None:
        print()
        print(f"Best algorithm: {best_result}")
    else:
        test_number, test_case = test_case_meta
        print(tabulate([[test_number, *test_case, best_result]],
                       headers=["Test Case", "Process Count", "Average Arrival Time", "Maximum Burst Time",
                                "Test Description", "Best Algorithm"],
                       tablefmt="fancy_grid"))
        print()
    print(f"Done in {execution_time:.3f} seconds.")
    return best_result


def show_execution_log(plot, algorithm: str, result: SimulationResult, process_colors: dict[str, str],
                       get_color: Callable[[str], str]):
    """Plot a Gantt chart from a simulation run result."""

    y_labels = []

    # average_completion_time, execution_log, starved_processes, processes, process_switches = result
    execution_log = result[1]
    processes = result[3]

    plot.barh(y="<None>", width=0)

    for process in processes:
        # wait time bar
        process_color = process_colors.get(process.name)
        if process_color is None:
            process_color = get_color(process.name)
        plot.barh(y=process.name, width=process.completion_time - process.arrival_time, left=process.arrival_time,
                  height=0.5, color='lightgrey', zorder=0)
        # burst time bar
        # color = matplotlib.colors.colorConverter.to_rgba(process_color, alpha=0.5)
        plot.barh(y=process.name, width=process.burst_time, left=process.arrival_time,
                  height=0.5, color=process_color, edgecolor="black", alpha=0.25, zorder=0)

    for start, end, process in execution_log:
        name = "<None>" if process is None else process.name
        plot.barh(y=name, width=max(end - start, 1), left=start, height=0.5,
                  color=process_colors[name],
                  edgecolor="black", zorder=1)
        y_labels.append(name)
    plot.set_xlabel("Time")
    plot.set_ylabel("Processes")
    plot.set_title(f"Gantt Chart ({algorithm})")


def present_results_gui(results: dict[str, SimulationResult]):
    """Present the results in the graphical user interface."""
    # algorithm_name, (average_completion_time, execution_log, _) = get_best_result(results)
    axes = plt.subplots(2, 2, figsize=(20, 12))[1]
    all_colors = [color for color in matplotlib.colors.CSS4_COLORS if
                  all(c not in color for c in ["white", "black", "grey", "gray", "silver"])]
    process_colors: dict[str, str] = {"<None>": "black"}

    def get_color(process_name: str):
        color = all_colors.pop(random.randrange(0, len(all_colors)))
        process_colors[process_name] = color
        return color

    for i, (algorithm_name, result) in enumerate(results.items()):
        plot = axes[i % 2, i // 2]  # type: ignore
        show_execution_log(plot, algorithm_name, result, process_colors, get_color)
    mng = plt.get_current_fig_manager()
    try:
        mng.window.showMaximized()
    except AttributeError:
        try:
            mng.window.attributes('-zoomed', True)
        except AttributeError as error:
            print("Could not maximise window:", error)
    plt.tight_layout()
    plt.show()


def run_tests(test_cases: list[TestCase]):
    best_algorithms: dict[str, set[int]] = {}
    for test_number, test_case in enumerate(test_cases, start=1):
        execution_time, results = timeit.timeit(
            functools.partial(repeat_simulation, DEFAULT_ITERATION_COUNT, *test_case),
            number=1)
        for result in results:
            best_algorithms.setdefault(result, set())
        best_result = present_results_cli(results, execution_time, (test_number, test_case))
        best_algorithms[best_result].add(test_number)
    table_data = [(alg, len(test_numbers),
                   (", " if len(test_numbers) == 0 or len(test_numbers) > MAX_SUMMARY_TEST_DESCRIPTIONS else "\n").join(
                       str(test) for test in test_numbers) or "—",
                   "(too many to display)" if len(test_numbers) > MAX_SUMMARY_TEST_DESCRIPTIONS else "—" if len(
                       test_numbers) == 0
                   else "\n".join(test_cases[test_number - 1][3] for test_number in test_numbers))
                  for alg, test_numbers in best_algorithms.items()]
    print(tabulate(table_data,
                   headers=["Best Algorithm", "Score", "Test Cases", "Test Description"], tablefmt="fancy_grid"))
