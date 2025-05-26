from abc import ABC, abstractmethod
from typing import List


class PageAllocationAlgorithm(ABC):
    def __init__(self, memory_size: int):
        self.memory_size = memory_size
        self.memory: List[int] = []
        self.page_faults = 0
        self.page_hits = 0
        self.history: List[List[int]] = []

    def run(self, sequence: List[int]) -> None:
        """
        Run the page replacement algorithm on the given sequence.
        """
        for page in sequence:
            self._process_page(page)
            self._record_memory_state()

    def _record_memory_state(self):
        """
        Optional: record a snapshot of the current memory state.
        Useful for debugging or visualization.
        """
        self.history.append(self.memory.copy())

    @abstractmethod
    def _process_page(self, page: int) -> None:
        """
        Must be implemented by subclasses.
        Process a single page reference.
        """
        pass

    def reset(self) -> None:
        """
        Reset state so the algorithm can be re-used.
        """
        self.memory.clear()
        self.page_faults = 0
        self.page_hits = 0
        self.history.clear()

    def stats(self) -> dict:
        """
        Return a dictionary of stats.
        """
        return {
            "page_faults": self.page_faults,
            "page_hits": self.page_hits,
            "memory_size": self.memory_size
        }
