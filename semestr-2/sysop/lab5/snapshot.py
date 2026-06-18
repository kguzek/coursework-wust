from dataclasses import dataclass


@dataclass
class ProcessorSnapshot:
    load: int
    active_processes: int
    load_queries: int
    delegated_processes: int


@dataclass
class SchedulerSnapshot:
    load_average: float
    load_standard_deviation: float
    total_load_queries: int
    total_delegated_processes: int
