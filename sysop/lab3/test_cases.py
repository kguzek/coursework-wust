from typing import List, Callable

from tabulate import tabulate

from lab3.algorithms.alru import ALRU
from lab3.algorithms.base import PageAllocationAlgorithm
from lab3.algorithms.fifo import FIFO
from lab3.algorithms.lru import LRU
from lab3.algorithms.opt import OPT
from lab3.algorithms.rand import Rand


class TestCase:
    def __init__(
            self,
            name: str,
            description: str,
            memory_size: int,
            sequence: List[int],
    ):
        self.name = name
        self.description = description
        self.memory_size = memory_size
        self.sequence = sequence

    def __repr__(self):
        return f"<TestCase {self.name} (memory={self.memory_size}, seq_len={len(self.sequence)})>"


def run_testcase_for_algos(testcase: TestCase, algos: List[Callable[[int], PageAllocationAlgorithm]]):
    print(f"Test case: {testcase.name}")
    print(f"Description: {testcase.description}")
    print(f"Memory size: {testcase.memory_size}")
    print(f"Sequence: {testcase.sequence}\n")

    results = []

    for algo_class in algos:
        algo = algo_class(testcase.memory_size)
        algo.run(testcase.sequence)
        stats = algo.stats()
        results.append(
            {
                "Algorithm": algo_class.__name__,
                "Page Faults": stats["page_faults"],
                "Page Hits": stats["page_hits"],
                "Thrashing Events": stats["thrashing_events"],
                "Locality Rate": f"{stats['locality_rate']:.2f}",
                "Avg. PFF": f"{stats['average_pff']:.2f}",
            }
        )

    print(tabulate(results, headers="keys", tablefmt="fancy_grid"))

    # Find minimum page faults
    min_faults = min(r["Page Faults"] for r in results)
    best_algos = [r["Algorithm"] for r in results if r["Page Faults"] == min_faults]

    if len(best_algos) == 1:
        print(f"\nBest algorithm: {best_algos[0]} with {min_faults} page faults.\n")
    else:
        tied_algos = ", ".join(best_algos)
        print(f"\nTie between algorithms: {tied_algos} with {min_faults} page faults each.\n")

    print("=" * 60 + "\n")


def run_all_testcases():
    testcases = [
        TestCase(
            name="Sequential Access",
            description=(
                "Pages accessed sequentially. "
                "Tests how algorithms handle high locality and simple patterns."
            ),
            memory_size=3,
            sequence=list(range(10)),
        ),
        TestCase(
            name="Looping Access",
            description=(
                "Pages accessed in a small loop repeatedly. "
                "Tests algorithms' ability to keep hot pages in memory."
            ),
            memory_size=3,
            sequence=[0, 1, 2, 0, 1, 2, 0, 1, 2],
        ),
        TestCase(
            name="Thrashing Scenario",
            description=(
                "Memory smaller than working set, causing frequent faults and thrashing. "
                "Tests thrashing detection and handling."
            ),
            memory_size=2,
            sequence=[0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
        ),
        TestCase(
            name="Random Access",
            description=(
                "Random page requests to evaluate randomness in RAND and resilience of others."
            ),
            memory_size=4,
            sequence=[3, 7, 2, 5, 1, 6, 4, 7, 3, 2, 5, 1],
        ),
        TestCase(
            name="Localized Bursts",
            description=(
                "Bursts of accesses to localized page ranges separated by jumps. "
                "Tests algorithms' ability to detect locality and adapt."
            ),
            memory_size=4,
            sequence=[1, 2, 3, 4, 1, 2, 3, 4, 10, 11, 12, 13, 10, 11, 12, 13],
        ),
        TestCase(
            name="OPT Advantage Highlight",
            description=(
                "Designed to show how OPT outperforms others by knowing future accesses."
            ),
            memory_size=3,
            sequence=[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5],
        ),
    ]

    algos = [ALRU, FIFO, LRU, OPT, Rand]

    for testcase in testcases:
        run_testcase_for_algos(testcase, algos)


if __name__ == "__main__":
    run_all_testcases()
