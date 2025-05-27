from tabulate import tabulate

from lab3.algorithms.lru import LRU
from lab3.config import generate_simulation_config, generate_page_request_sequence
from lab4.strategies.base import FrameAllocationStrategy
from lab4.strategies.equal import EqualAllocation
from lab4.strategies.frequency import PageFaultFrequency
from lab4.strategies.proportional import ProportionalAllocation
from lab4.strategies.working_set import WorkingSetModel

STRATEGIES = {
    "Proportional Allocation": ProportionalAllocation(),
    "Equal Allocation": EqualAllocation(),
    "Page Fault Frequency": PageFaultFrequency(),
    "Working Set Model": WorkingSetModel(),
}


class MultiProcessLRUSimulator:
    def __init__(self, total_frames: int, processes: dict[str, list[int]], strategy: FrameAllocationStrategy):
        self.total_frames = total_frames
        self.processes = processes
        self.strategy = strategy
        self.algorithms: dict[str, LRU] = {}
        self.allocations: dict[str, int] = {}
        self.allocate()

    def allocate(self):
        self.allocations = self.strategy.allocate(self.total_frames, self.processes)

    def run(self) -> dict[str, dict]:
        results = {}
        for pid, sequence in self.processes.items():
            frames = self.allocations[pid]
            lru = LRU(memory_size=frames)
            lru.run(sequence, self.allocate)
            self.algorithms[pid] = lru
            results[pid] = lru.stats()
        return results

    def print_results(self):
        results = self.run()

        table = []
        total_faults = total_hits = total_requests = total_thrashing = 0

        for pid, stats in results.items():
            faults = stats["page_faults"]
            hits = stats["page_hits"]
            thrashing = stats["thrashing_events"]
            requests = faults + hits
            total_faults += faults
            total_hits += hits
            total_requests += requests
            total_thrashing += thrashing
            table.append([pid, self.allocations[pid], faults, hits, thrashing, requests])

        table.append(["Total", self.total_frames, total_faults, total_hits, total_thrashing, total_requests])

        headers = ["PID", "Frames", "Page Faults", "Page Hits", "Thrashing Events", "Requests"]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def generate_processes(num_processes: int = 10) -> dict[str, list[int]]:
    return {
        f"P{i}": generate_page_request_sequence(generate_simulation_config(None, 500, 1500))
        for i in range(1, num_processes + 1)
    }


def main():
    processes = generate_processes()
    total_frames = 100

    for name, strategy in STRATEGIES.items():
        print(f"\n[{name}]")
        simulator = MultiProcessLRUSimulator(
            total_frames=total_frames,
            processes=processes,
            strategy=strategy
        )
        simulator.print_results()


if __name__ == "__main__":
    main()
