import random
from abc import ABC, abstractmethod
from typing import Iterable

from lab5.process import Process
from lab5.processor import Processor
from lab5.snapshot import ProcessorSnapshot, SchedulerSnapshot


def standard_deviation(mean: float, values: Iterable[float]) -> float:
    total_values = 0
    sigma = 0
    for value in values:
        total_values += 1
        sigma += (value - mean) ** 2
    return (sigma / total_values) ** 0.5


class ConcurrentProcessScheduler(ABC):
    def __init__(self, processors: list[Processor], processor_load_threshold: int):
        self.processor_load_threshold: int = processor_load_threshold
        self.processors: list[Processor] = [processor.copy() for processor in processors]
        self.current_time: int = 0
        self.has_pending_processes: bool = True
        self.statistics: list[tuple[list[ProcessorSnapshot], SchedulerSnapshot]] = []

    def get_candidate_processors(self, excluded_processor: Processor) -> list[Processor]:
        candidate_processors = self.processors.copy()
        candidate_processors.remove(excluded_processor)
        return candidate_processors

    @staticmethod
    def select_random_processor(candidate_processors: list[Processor]) -> Processor:
        return candidate_processors.pop(random.randrange(len(candidate_processors)))

    @abstractmethod
    def select_target_processor(self, initial_processor: Processor, process: Process) -> tuple[Processor, int] | None:
        """Selects the appropriate processor to use to schedule the given process.

        Returns a tuple containing the selected processor and its current system load as a percentage."""

    def tick(self) -> None:
        self.has_pending_processes = False
        for processor in self.processors:
            for process in processor.get_pending_processes(self.current_time):
                self.has_pending_processes = True
                target_processor, _ = self.select_target_processor(processor, process)
                if target_processor is None:
                    processor.queued_processes.insert(0, process)
                    break
                if processor is not target_processor:
                    processor.processes_delegated += 1
                target_processor.assign_process(process)
            for process in processor.active_processes:
                self.has_pending_processes = True
                process.tick()
            # remove completed processes
            processor.active_processes = [process for process in processor.active_processes if process.is_running()]
        self.record_statistics()
        self.current_time += 1

    def record_statistics(self) -> None:
        total_load = 0
        total_load_queries = 0
        total_delegated_processes = 0
        processor_snapshots: list[ProcessorSnapshot] = []
        for processor in self.processors:
            snapshot = processor.snapshot()
            total_load += snapshot.load
            total_load_queries += snapshot.load_queries
            total_delegated_processes += snapshot.delegated_processes
            processor_snapshots.append(snapshot)
        num_processors = len(self.processors)
        load_average = total_load / num_processors
        load_standard_deviation = standard_deviation(load_average, (snapshot.load for snapshot in processor_snapshots))
        scheduler_snapshot = SchedulerSnapshot(
            load_average=load_average,
            load_standard_deviation=load_standard_deviation,
            total_load_queries=total_load_queries,
            total_delegated_processes=total_delegated_processes,
        )
        self.statistics.append((processor_snapshots, scheduler_snapshot))

    def run(self):
        while self.has_pending_processes:
            self.tick()

    def __repr__(self):
        return self.__class__.__name__
