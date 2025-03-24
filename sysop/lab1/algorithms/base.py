from abc import abstractmethod

from ..common import get_queued_processes, reset_processes, has_incomplete_processes, calculate_average_completion_time
from ..process import Process

DEBUG_MODE = True


def log(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)


class Algorithm:
    """Base class for scheduling algorithms"""

    def __init__(
            self,
            processes: list[Process],
            tick_duration: int = 1,
            starvation_threshold: int = 200,
    ):
        self.current_time = 0
        self.current_process: Process | None = None
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

    def log_queue(self, current_time: float = None):
        time = self.current_time if current_time is None else current_time
        log(f"{time=:.1f}s, queue={self.queue}")

    def tick(self):
        """Progresses the simulation by one tick"""
        self.queue = get_queued_processes(self.processes, self.current_time)
        self.log_queue()
        self.current_time += 1
        self.current_process = self.select_current_process()
        for process in self.queue:
            process.tick(self.current_time, self.tick_duration)
            if process.wait_time - process.burst_time > self.starvation_threshold:
                self.starved_processes.add(process)
                # process.complete(self.current_time)
        if self.previous_process_id is None or self.previous_process_id != id(
                self.current_process
        ):
            self.process_switches += 1
            self.previous_process_id = id(self.current_process)
        if self.current_process is not None:
            self.current_process.process(self.current_time, self.tick_duration)
            if self.current_process.is_complete:
                self.current_process = None
        self.log_queue(self.current_time + 0.5)

    def run(self):
        """
        Runs the simulation loop until all processes are complete.

        Returns the average completion time of each process.
        """
        log(f"Running {self.__class__.__name__} algorithm...")
        reset_processes(self.processes)
        while has_incomplete_processes(self.processes):
            self.tick()
        return (
            calculate_average_completion_time(self.processes),
            self.process_switches,
            len(self.starved_processes),
        )
