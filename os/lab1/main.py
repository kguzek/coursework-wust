"""Main module to run scheduling algorithms"""

import random

from .algorithms.fcfs import FCFS
from .algorithms.rr import RR
from .algorithms.sjf import SJF
from .algorithms.srtf import SRTF
from .process import Process

TIME_QUANTUM = 2


def generate_processes(process_count: int):
    """Generate random processes"""
    processes: list[Process] = []
    for _ in range(process_count):
        burst_time = random.randint(1, 10)
        arrival_time = random.randint(0, 20)
        processes.append(Process(arrival_time, burst_time))
    return processes


def main():
    """Entry point of the program"""
    process_count = 0
    while process_count <= 0:
        input_str = input("Number of processes: ")
        try:
            process_count = int(input_str)
        except ValueError:
            print(f"Invalid input '{input_str}'. Please enter a positive integer.")
    processes = generate_processes(process_count)

    results = {
        "first come first serve": FCFS(processes).run(),
        "shortest job first": SJF(processes).run(),
        "shortest remaining time first": SRTF(processes).run(),
        "round robin": RR(processes, TIME_QUANTUM).run(),
    }

    results = dict(sorted(results.items(), key=lambda item: item[1][0]))

    def serialise_result(result: tuple[float, int, int]):
        """Serialise the result tuple into a string"""

        average_completion_time, process_switches, starved_processes = result
        return (
            f"{average_completion_time = :.2f}, {process_switches = }, "
            f"{starved_processes = }/{process_count}"
        )

    padding = len(max(results)) + 5
    longest_time = max(results.values(), key=lambda i: i[0])
    longest_time_length = len(serialise_result(longest_time))
    output_length = padding + longest_time_length
    print("-" * output_length)

    for algorithm, algorithm_result in results.items():
        label = f"{algorithm}:"
        print(f"{label:<{padding}}{serialise_result(algorithm_result):>{longest_time_length}}")

    print("-" * output_length)
    best_algorithm = min(results, key=lambda i: results[i][0])
    print(f"{best_algorithm = }")


if __name__ == "__main__":
    main()
