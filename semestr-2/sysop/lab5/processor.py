from typing import Generator, Self

from lab5.process import Process
from lab5.snapshot import ProcessorSnapshot


class Processor:
    def __init__(self, queued_processes: list[Process]):
        self.times_queried: int = 0
        self.processes_delegated: int = 0
        self.queued_processes: list[Process] = queued_processes
        self.queued_processes.sort(key=lambda p: p.arrival_time)
        self.active_processes: list[Process] = []
        self.postponed_processes: int = 0

    def would_overload(self, candidate_process: Process) -> bool:
        """Checks if handling the given candidate process would cause the CPU to overload."""
        return candidate_process.load_burden + self._get_load() > 100

    def ensure_no_overload(self, candidate_process: Process) -> None:
        """Throws an exception if handling the given process would cause it to overload."""
        if self.would_overload(candidate_process):
            raise RuntimeError(f"CPU assignment of {candidate_process} caused {self} to overload!")

    def assign_process(self, process: Process) -> None:
        self.ensure_no_overload(process)
        self.active_processes.append(process)

    def get_pending_processes(self, current_time: int) -> Generator[Process, None, None]:
        while len(self.queued_processes) > 0:
            if not self.queued_processes[0].is_active(current_time):
                break
            yield self.queued_processes.pop(0)

    def _get_load(self) -> int:
        """Calculates the current system load of the processor in the discrete range [0, 100]."""
        return sum(process.load_burden for process in self.active_processes)

    def query_load(self) -> int:
        """Queries the processor load as a percentage and increments the query counter by 1."""
        self.times_queried += 1
        load = self._get_load()
        return load

    def snapshot(self) -> ProcessorSnapshot:
        return ProcessorSnapshot(
            load=self._get_load(),
            active_processes=len(self.active_processes),
            load_queries=self.times_queried,
            delegated_processes=self.processes_delegated,
        )

    def __repr__(self):
        return f"Processor(load={self._get_load()}, active_processes={len(self.active_processes)})"

    def copy(self) -> Self:
        return Processor(queued_processes=[process.copy() for process in self.queued_processes])
