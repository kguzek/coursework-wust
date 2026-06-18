"""Main module to run scheduling algorithms"""

import timeit

import sys

from lab1.common import DEFAULT_ITERATION_COUNT, TestCase
from lab1.simulation import repeat_simulation, present_results_cli, present_results_gui, run_simulation, run_tests

# Allows capturing the return value of the timeit function
timeit.template = """
def inner(_it, _timer{init}):
    {setup}
    _t0 = _timer()
    for _i in _it:
        retval = {stmt}
    _t1 = _timer()
    return _t1 - _t0, retval
"""

# (process count, average arrival time, max burst time, description)
TEST_CASES: list[TestCase] = [
    (5, 1, 5, "Few short jobs arriving quickly."),
    (5, 10, 50, "Few long jobs arriving slowly."),
    (10, 2, 10, "Moderate number of mixed jobs arriving frequently."),
    (10, 10, 5, "Many short jobs but arriving sparsely."),
    (10, 5, 20, "Balanced mix of short and long jobs."),
    (20, 1, 5, "Many very short jobs, frequent arrivals (stress test SJF/SRTF)."),
    (20, 5, 50, "Many long jobs with moderate arrivals."),
    (20, 10, 20, "Even distribution of jobs, moderate scheduling challenge."),
    (20, 15, 50, "Long jobs with a few arriving late."),
    (50, 1, 5, "Very high process count, all short jobs, rapid arrivals."),
    (50, 5, 50, "High process count with varied burst times."),
    (50, 10, 10, "Many small jobs arriving in a controlled manner."),
    (50, 20, 50, "Large batch of mostly long jobs, challenging RR."),
    (10, 1, 50, "Few jobs, one very long job early (tests starvation risk)."),
    (10, 10, 1, "All jobs are extremely short, with moderate spacing."),
    (20, 10, 50, "Mixed job sizes, but spaced arrivals."),
    (20, 1, 50, "One long job among many short ones (tests RR effectiveness)."),
    (5, 5, 5, "Small balanced case, baseline performance check."),
    (10, 3, 30, "Mid-range challenge with varied burst times."),
    (50, 10, 5, "Many short jobs but slow arrivals, testing FCFS fairness."),
]


def input_process_count():
    process_count = 0
    while process_count <= 0:
        input_str = input("Number of processes: ")
        try:
            process_count = int(input_str)
        except ValueError:
            print(f"Invalid input '{input_str}'. Please enter a positive integer.")
    return process_count


def run_iterations(process_count: int):
    iterations: int = DEFAULT_ITERATION_COUNT
    if len(sys.argv) > 2:
        raw_iterations = sys.argv[sys.argv.index("-r") + 1]
        try:
            iterations = int(raw_iterations)
            if iterations <= 0:
                raise ValueError
        except ValueError:
            print(f"Invalid iteration '{raw_iterations}'. Using default value of 30.")
    print(f"Running {iterations} simulation iterations with {process_count} processes...")
    return repeat_simulation(iterations, process_count)


def main():
    """Entry point of the program."""
    test_mode = "-t" in sys.argv
    iterated_mode = "-r" in sys.argv
    if test_mode:
        run_tests(TEST_CASES)
        return
    process_count = input_process_count()
    if process_count > 50:
        # prevent the matplotlib charts from being rendered with many processes
        iterated_mode = True
    func = run_iterations if iterated_mode else run_simulation
    execution_time, results = timeit.timeit(lambda: func(process_count), number=1)
    present_results_cli(results, execution_time)
    if not iterated_mode:
        present_results_gui(results)


if __name__ == "__main__":
    main()
