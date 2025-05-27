import matplotlib.pyplot as plt
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


def populate_tables(setup: tuple[str, list[str]], faults_list: list[int], hits_list: list[int],
                    thrashing_list: list[int], frames_list: list[int]):
    strategy_name, pids = setup

    # ==== Matplotlib Figure ====
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(f"Memory Allocation Strategy: {strategy_name}", fontsize=16)

    # Page Faults
    axs[0, 0].bar(pids, faults_list, color="crimson")
    axs[0, 0].set_title("Page Faults per Process")
    axs[0, 0].set_xlabel("Process ID")
    axs[0, 0].set_ylabel("Page Faults")
    axs[0, 0].grid(True, axis="y")

    # Hits vs Faults
    x = range(len(pids))
    bar_width = 0.4
    axs[0, 1].bar(x, faults_list, width=bar_width, label="Faults", color="salmon")
    axs[0, 1].bar([i + bar_width for i in x], hits_list, width=bar_width, label="Hits", color="seagreen")
    axs[0, 1].set_xticks([i + bar_width / 2 for i in x])
    axs[0, 1].set_xticklabels(pids)
    axs[0, 1].set_title("Hits vs Faults per Process")
    axs[0, 1].set_xlabel("Process ID")
    axs[0, 1].set_ylabel("Count")
    axs[0, 1].legend()
    axs[0, 1].grid(True, axis="y")

    # Thrashing Events
    axs[1, 0].bar(pids, thrashing_list, color="steelblue")
    axs[1, 0].set_title("Thrashing Events per Process")
    axs[1, 0].set_xlabel("Process ID")
    axs[1, 0].set_ylabel("Thrashing Events")
    axs[1, 0].grid(True, axis="y")

    # Frame Allocation Pie Chart
    axs[1, 1].pie(frames_list, labels=pids, autopct="%1.1f%%", startangle=140, colors=plt.cm.tab20.colors)
    axs[1, 1].set_title("Frame Allocation per Process")


class MultiProcessLRUSimulator:
    def __init__(self, total_frames: int, processes: dict[str, list[int]], strategy: FrameAllocationStrategy):
        self.total_frames = total_frames
        self.processes = processes
        self.strategy = strategy
        self.strategy_name = type(strategy).__name__
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

        # For charts
        pids = []
        faults_list = []
        hits_list = []
        thrashing_list = []
        frames_list = []

        for pid, stats in results.items():
            faults = stats["page_faults"]
            hits = stats["page_hits"]
            thrashing = stats.get("thrashing_events", 0)
            requests = faults + hits

            pids.append(pid)
            faults_list.append(faults)
            hits_list.append(hits)
            thrashing_list.append(thrashing)
            frames_list.append(self.allocations[pid])

            total_faults += faults
            total_hits += hits
            total_requests += requests
            total_thrashing += thrashing

            table.append([pid, self.allocations[pid], faults, hits, thrashing, requests])

        table.append(["Total", self.total_frames, total_faults, total_hits, total_thrashing, total_requests])

        headers = ["PID", "Frames", "Page Faults", "Page Hits", "Thrashing Events", "Requests"]
        print("\n" + tabulate(table, headers=headers, tablefmt="fancy_grid"))

        populate_tables((self.strategy_name, pids), faults_list, hits_list, thrashing_list, frames_list)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()


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
