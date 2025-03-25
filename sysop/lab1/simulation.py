"""Simulation module for the CPU scheduling algorithms."""

import random
from concurrent.futures import as_completed, ProcessPoolExecutor

import matplotlib
from matplotlib import pyplot as plt
from tabulate import tabulate

from .algorithms.fcfs import FCFS
from .algorithms.rr import RR
from .algorithms.sjf import SJF
from .algorithms.srtf import SRTF
from .common import generate_processes, SimulationResult

TIME_QUANTUM = 2


def run_simulation(process_count: int) -> dict[str, SimulationResult]:
    """Run the simulation for all algorithms with the given number of processes.
    :return the run results for each algorithm, formatted as: average_completion_time, execution_log, starved_processes, processes."""

    processes = generate_processes(process_count)

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


def repeat_simulation(process_count: int, iterations: int) -> dict[str, SimulationResult]:
    all_results: dict[str, list[SimulationResult]] = {}

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(run_simulation, process_count) for _ in range(iterations)
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


def present_results_cli(results: dict[str, SimulationResult], execution_time: float):
    """Present the results in the command line interface."""

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

    print()
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
    print()
    print(f"Best algorithm: {get_best_result(results)[0]}")
    print(f"Done in {execution_time:.3f} seconds.")


def show_execution_log(plot, algorithm: str, result: SimulationResult):
    """Plot a Gantt chart from an execution log.
       execution_log: list of tuples (start_time, end_time, process_name)
    """

    y_labels = []

    average_completion_time, execution_log, starved_processes, processes, process_switches = result
    all_colors = [color for color in matplotlib.colors.CSS4_COLORS.keys() if
                  all(c not in color for c in ["white", "black", "grey", "gray", "silver"])]
    process_colors: dict[str, str] = {"<None>": "black"}

    plot.barh(y="<None>", width=0)

    for process in processes:
        # wait time bar
        process_color = all_colors.pop(random.randrange(0, len(all_colors)))
        process_colors[process.name] = process_color
        plot.barh(y=process.name, width=process.completion_time - process.arrival_time, left=process.arrival_time,
                  height=0.5, color='lightgrey', zorder=0)
        # burst time bar
        # color = matplotlib.colors.colorConverter.to_rgba(process_color, alpha=0.5)
        plot.barh(y=process.name, width=process.burst_time, left=process.arrival_time,
                  height=0.5, color=process_color, edgecolor="black", alpha=0.25, zorder=0)

    for idx, (start, end, process) in enumerate(execution_log):
        name = "<None>" if process is None else process.name
        plot.barh(y=name, width=max(end - start, 1), left=start, height=0.5,
                  color=process_colors[name],
                  edgecolor='black', zorder=1)
        y_labels.append(name)
    plot.set_xlabel("Time")
    plot.set_ylabel("Processes")
    plot.set_title(f"Gantt Chart ({algorithm})")


def present_results_gui(results: dict[str, SimulationResult]):
    """Present the results in the graphical user interface."""
    # algorithm_name, (average_completion_time, execution_log, _) = get_best_result(results)
    fig, axes = plt.subplots(2, 2, figsize=(20, 12))
    for i, (algorithm_name, result) in enumerate(results.items()):
        plot = axes[i % 2, i // 2]  # type: ignore
        show_execution_log(plot, algorithm_name, result)
    mng = plt.get_current_fig_manager()
    mng.window.attributes('-zoomed', True)
    plt.tight_layout()
    plt.show()
