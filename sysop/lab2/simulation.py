import random

from lab2.algorithms.fcfs import FCFS
from lab2.request import DiskAccessRequest
from lab2.visualizer import SimulationVisualizer


def generate_request(average_arrival_time: float, total_chambers: int) -> DiskAccessRequest:
    chamber = random.randint(1, total_chambers)
    arrival_time = int(random.expovariate(1 / average_arrival_time))

    return DiskAccessRequest(chamber, arrival_time)


def generate_requests(process_count: int, total_chambers: int, average_arrival_time: float = None) -> list[
    DiskAccessRequest]:
    return [
        generate_request(process_count ** 1.5 if average_arrival_time is None else average_arrival_time, total_chambers)
        for _ in range(process_count)]


def run_simulation(total_chambers: int):
    requests = generate_requests(10, total_chambers)

    algorithms = {
        "FCFS": FCFS(requests, num_chambers=total_chambers)
    }

    visualizer = SimulationVisualizer()

    for name, algorithm in algorithms.items():
        print("Running algorithm", name)
        visualizer.run(algorithm)
