from abc import ABC, abstractmethod
from collections import deque
from typing import List


class PageAllocationAlgorithm(ABC):
    def __init__(
            self,
            memory_size: int,
            thrashing_window: int = 5,
            thrashing_threshold: int = 4,
            pff_window: int = 5,
    ):
        self.memory_size = memory_size
        self.memory: List[int] = []
        self.page_faults = 0
        self.page_hits = 0
        self.history: List[List[int]] = []

        self.thrashing_window = thrashing_window
        self.thrashing_threshold = thrashing_threshold
        self.recent_faults = deque(maxlen=thrashing_window)
        self.thrashing_events = 0

        self.last_page: int | None = None
        self.locality_hits = 0

        self.pff_window = pff_window
        self.pff_faults = deque(maxlen=pff_window)
        self.pff_values: List[float] = []

        self.sequence: List[int] = []

    def run(self, sequence: List[int]) -> None:
        """
        Run the page replacement algorithm on the given sequence.
        """
        self.reset()  # clear previous state
        self.sequence = sequence

        for idx, page in enumerate(sequence):
            if self.last_page is not None and abs(page - self.last_page) <= 1:
                self.locality_hits += 1
            self.last_page = page

            before_faults = self.page_faults
            self._process_page(page, idx)
            fault_occurred = (self.page_faults > before_faults)

            self.recent_faults.append(1 if fault_occurred else 0)
            if sum(self.recent_faults) >= self.thrashing_threshold:
                self.thrashing_events += 1

            self.pff_faults.append(1 if fault_occurred else 0)
            if len(self.pff_faults) == self.pff_window:
                pff = sum(self.pff_faults) / self.pff_window
                self.pff_values.append(pff)

            self._record_memory_state()

    def _record_memory_state(self):
        """
        Optional: record a snapshot of the current memory state.
        Useful for debugging or visualization.
        """
        self.history.append(self.memory.copy())

    @abstractmethod
    def _process_page(self, page: int, current_index: int) -> None:
        """
        Must be implemented by subclasses.
        Process a single page reference.
        current_index is the position in the sequence, used by algorithms like OPT.
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

        self.recent_faults.clear()
        self.thrashing_events = 0

        self.last_page = None
        self.locality_hits = 0

        self.pff_faults.clear()
        self.pff_values.clear()

        self.sequence.clear()

    def stats(self) -> dict:
        total_requests = len(self.sequence) if self.sequence else 0
        locality_rate = self.locality_hits / total_requests if total_requests else 0
        average_pff = (
            sum(self.pff_values) / len(self.pff_values) if self.pff_values else 0
        )

        return {
            "page_faults": self.page_faults,
            "page_hits": self.page_hits,
            "memory_size": self.memory_size,
            "thrashing_events": self.thrashing_events,
            "locality_rate": locality_rate,
            "average_pff": average_pff,
        }
