"""Main module to run scheduling algorithms"""

import random
from abc import abstractmethod


class Process:
    """Process class to store process information"""

    def __init__(self, arrival_time, burst_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0
        self.complete = False

    def reset(self):
        """Reset the process to initial state"""
        self.remaining_time = self.burst_time
        self.wait_time = 0
        self.complete = False

    def tick(self, time=1):
        """Perform a tick of the process"""
        if not self.complete:
            self.wait_time += time

    def process(self, time=1):
        """Perform the process for given time"""
        if self.remaining_time <= time:
            self.remaining_time = 0
            self.complete = True
        else:
            self.remaining_time -= time

    def __lt__(self, other):
        return self.remaining_time < other.remaining_time


def has_incomplete_processes(processes: list[Process]):
    """Check if there are any incomplete processes"""
    return any(not process.complete for process in processes)


def calculate_average_completion_time(processes: list[Process]):
    """Calculate the average completion time of processes"""
    return sum(process.wait_time for process in processes) / len(processes)


def get_queued_processes(processes: list[Process], current_time: int):
    """Get the processes that have arrived in the queue and are incomplete"""
    return [
        process
        for process in processes
        if process.arrival_time <= current_time and not process.complete
    ]


def reset_processes(processes: list[Process]):
    """Resets the processes to their initial state and sorts them by arrival time"""
    for process in processes:
        process.reset()
    processes.sort(key=lambda x: x.arrival_time)


class Algorithm:
    """Base class for scheduling algorithms"""

    def __init__(
        self,
        processes: list[Process],
        tick_duration: int = 1,
        starvation_threshold: int = 200,
    ):
        self.current_time = 0
        self.current_process: Process = None
        self.process_switches = 0
        self.previous_process_id = None
        self.queue: list[Process] = []
        self.starved_processes = set()
        self.processes = processes.copy()
        self.tick_duration = tick_duration
        self.starvation_threshold = starvation_threshold

    @abstractmethod
    def select_current_process(self) -> Process | None:
        """Selects the current process to be executed, if any"""

    def tick(self):
        """Progresses the simulation by one tick"""
        self.queue = get_queued_processes(self.processes, self.current_time)
        self.current_time += 1
        self.current_process = self.select_current_process()
        for process in self.queue:
            process.tick(self.tick_duration)
            if process.wait_time - process.burst_time > self.starvation_threshold:
                self.starved_processes.add(process)
                # process.complete = True
        if self.previous_process_id is None or self.previous_process_id != id(
            self.current_process
        ):
            self.process_switches += 1
            self.previous_process_id = id(self.current_process)
        if self.current_process is not None:
            self.current_process.process(self.tick_duration)
            if self.current_process.complete:
                self.current_process = None

    def run(self):
        """
        Runs the simulation loop until all processes are complete.

        Returns the average completion time of each process.
        """
        # print(f"Running {self.__class__.__name__} algorithm")
        reset_processes(self.processes)
        while has_incomplete_processes(self.processes):
            self.tick()
        return (
            calculate_average_completion_time(self.processes),
            self.process_switches,
            len(self.starved_processes),
        )


class FCFS(Algorithm):
    """First-Come, First-Served (FCFS) scheduling algorithm"""

    def select_current_process(self):
        return self.queue[0] if len(self.queue) > 0 else None


class SJF(Algorithm):
    """Shortest Job First (SJF) scheduling algorithm"""

    def select_current_process(self):
        self.queue.sort(key=lambda x: x.burst_time)
        return (
            self.current_process
            if self.current_process is not None
            else self.queue[0] if len(self.queue) > 0 else None
        )


class SRTF(Algorithm):
    """Shortest Remaining Time First (SRTF) scheduling algorithm"""

    def select_current_process(self):
        self.queue.sort(key=lambda x: x.remaining_time)
        return self.queue[0] if len(self.queue) > 0 else None


class RR(Algorithm):
    """Round Robin (RR) scheduling algorithm"""

    def select_current_process(self):
        if len(self.queue) == 0:
            return None
        if self.previous_process_id is None:
            return self.queue[0]
        for process in self.queue:
            if id(process) != self.previous_process_id:
                return process
        return None


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
    time_quantum = 2

    results = {
        "first come first serve": FCFS(processes).run(),
        "shortest job first": SJF(processes).run(),
        "shortest remaining time first": SRTF(processes).run(),
        "round robin": RR(processes, time_quantum).run(),
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

    for algorithm, result in results.items():
        label = f"{algorithm}:"
        print(f"{label:<{padding}}{serialise_result(result):>{longest_time_length}}")

    print("-" * output_length)
    best_algorithm = min(results, key=lambda i: results[i][0])
    print(f"{best_algorithm = }")


if __name__ == "__main__":
    main()