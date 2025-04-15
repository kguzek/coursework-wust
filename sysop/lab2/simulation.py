import random

from lab2.algorithms.base import DiskAccessAlgorithm
from lab2.algorithms.cscan import CScan
from lab2.algorithms.edf import EDF
from lab2.algorithms.fcfs import FCFS
from lab2.algorithms.fdscan import FDScan
from lab2.algorithms.scan import Scan
from lab2.algorithms.sstf import SSTF
from lab2.request import DiskAccessRequest
from lab2.visualizer import SimulationVisualizer

DEFAULT_REQUEST_COUNT: int = 30
DEFAULT_DEADLINE_PROBABILITY: float = 0.3
DEFAULT_CHAMBER_TOTAL: int = 100
MINIMUM_DEADLINE: int = 30


def generate_request(average_arrival_time: float, total_chambers: int, include_deadline: bool) -> DiskAccessRequest:
    chamber = random.randint(1, total_chambers)
    arrival_time = int(random.expovariate(1 / average_arrival_time))

    deadline = int(random.expovariate(1 / total_chambers) + MINIMUM_DEADLINE) if include_deadline else -1
    return DiskAccessRequest(chamber, arrival_time, deadline)


def generate_requests(request_count: int, total_chambers: int, average_arrival_time: float = None,
                      deadline_probability: float = 0) -> list[DiskAccessRequest]:
    return [
        generate_request(request_count ** 1.5 if average_arrival_time is None else average_arrival_time, total_chambers,
                         random.random() < deadline_probability)
        for _ in range(request_count)]


def run_algorithms(algorithms: dict[str, DiskAccessAlgorithm]) -> None:
    visualizer = SimulationVisualizer()
    for name, algorithm in algorithms.items():
        print("Running algorithm", name)
        visualizer.run(algorithm)
        print("Finish time:", algorithm.current_time)


def run_simulation_with_deadlines(total_chambers: int = DEFAULT_CHAMBER_TOTAL,
                                  request_count: int = DEFAULT_REQUEST_COUNT,
                                  deadline_probability: float = DEFAULT_DEADLINE_PROBABILITY):
    requests = generate_requests(request_count, total_chambers, None, deadline_probability)
    algorithms = {
        "EDF": EDF(requests, num_chambers=total_chambers),
        "FD-SCAN": FDScan(requests, num_chambers=total_chambers),
    }
    run_algorithms(algorithms)


def run_simulation(total_chambers: int = DEFAULT_CHAMBER_TOTAL, request_count: int = DEFAULT_REQUEST_COUNT):
    requests = generate_requests(request_count, total_chambers)
    algorithms = {
        "FCFS": FCFS(requests, num_chambers=total_chambers),
        "SSTF": SSTF(requests, num_chambers=total_chambers),
        "SCAN": Scan(requests, num_chambers=total_chambers),
        "C-SCAN": CScan(requests, num_chambers=total_chambers),
    }
    run_algorithms(algorithms)
