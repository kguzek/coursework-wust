import copy
from abc import abstractmethod

from ..common import get_queued_processes, calculate_average_completion_time, SimulationResult, DEBUG_MODE
from ..process import Process


class Algorithm:
    """Base class for scheduling algorithms"""

    def __init__(
            self,
            processes: list[Process],
            tick_duration: int = 1,
            starvation_threshold: int = 20,
            debug_mode: bool = DEBUG_MODE
    ):
        self.current_time = 0
        self.current_process: Process | None = None
        self.last_process_switch_time = 0
        self.execution_log: list[tuple[int, int, Process]] = []
        self.previous_process = None
        self.queue: list[Process] = []
        self.starved_processes = set()
        self.processes = copy.deepcopy(processes)
        self.tick_duration = tick_duration
        self.starvation_threshold = starvation_threshold
        self.debug_mode = debug_mode
        self.completed_processes = 0

    def log(self, message):
        if self.debug_mode:
            print(f"[{self.__class__.__name__}] {message}")

    @abstractmethod
    def select_current_process(self) -> Process | None:
        """Selects the current process to be executed, if any"""

    def log_queue(self, current_time: float = None):
        time = self.current_time if current_time is None else current_time
        self.log(f"({time:.1f}) {self.current_process}")

    def log_current_execution(self):
        """Adds the current execution to the execution log."""
        self.execution_log.append((self.last_process_switch_time, self.current_time, self.previous_process))

    def update_queue(self) -> None:
        """Updates the queue of processes that have arrived and are incomplete. Can be overridden for other data structures."""
        self.queue = get_queued_processes(self.processes, self.current_time)

    def tick(self):
        """Progresses the simulation by one tick"""
        self.update_queue()
        self.log_queue()
        self.current_time += self.tick_duration
        self.current_process = self.select_current_process()
        for process in self.queue:
            process.tick(self.tick_duration)
            if process.wait_time - process.burst_time > self.starvation_threshold:
                self.starved_processes.add(process)
                # process.complete(self.current_time)
        if self.previous_process != self.current_process:
            self.log_current_execution()
            self.previous_process = self.current_process
            self.last_process_switch_time = self.current_time
        if self.current_process is not None:
            self.current_process.process(self.current_time, self.tick_duration)
            if self.current_process.is_complete:
                self.current_process = None
                self.completed_processes += 1
        self.log_queue(self.current_time + 0.5)

    def run(self) -> SimulationResult:
        """
        Runs the simulation loop until all processes are complete.

        Returns the average completion time of each process.
        """
        self.log(f"Starting simulation with {len(self.processes)} processes.")
        while self.completed_processes < len(self.processes):
            self.tick()
        self.tick()
        return (
            calculate_average_completion_time(self.processes),
            self.execution_log,
            len(self.starved_processes),
            self.processes,
            len(self.execution_log)
        )
