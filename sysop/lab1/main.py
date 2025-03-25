"""Main module to run scheduling algorithms"""

import sys

import timeit

from .simulation import repeat_simulation, present_results_cli, present_results_gui, run_simulation

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
    iterations: int = 30
    if len(sys.argv) > 2:
        raw_iterations = sys.argv[sys.argv.index("-r") + 1]
        try:
            iterations = int(raw_iterations)
            if iterations <= 0:
                raise ValueError
        except ValueError:
            print(f"Invalid iteration '{raw_iterations}'. Using default value of 30.")
    print(f"Running {iterations} simulation iterations with {process_count} processes...")
    return repeat_simulation(process_count, iterations)


def main():
    """Entry point of the program."""
    iterated_mode = "-r" in sys.argv
    process_count = input_process_count()
    func = run_iterations if iterated_mode else run_simulation
    execution_time, results = timeit.timeit(lambda: func(process_count), number=1)
    present_results_cli(results, execution_time)
    if not iterated_mode:
        present_results_gui(results)


if __name__ == "__main__":
    main()
