from collections import deque

from lab3.algorithms.base import PageAllocationAlgorithm


class ALRU(PageAllocationAlgorithm):
    def __init__(self, memory_size: int):
        super().__init__(memory_size)
        self.queue: deque[int] = deque()
        self.reference_bits: dict[int, bool] = {}

    def _process_page(self, page: int) -> None:
        if page in self.memory:
            self.page_hits += 1
            self.reference_bits[page] = True
            return

        self.page_faults += 1

        if len(self.memory) < self.memory_size:
            self.memory.append(page)
            self.queue.append(page)
            self.reference_bits[page] = False
        else:
            while True:
                candidate = self.queue[0]
                if self.reference_bits.get(candidate, False):
                    self.reference_bits[candidate] = False
                    self.queue.rotate(-1)  # Move to the back
                else:
                    self.queue.popleft()
                    self.memory.remove(candidate)
                    del self.reference_bits[candidate]
                    break

            self.memory.append(page)
            self.queue.append(page)
            self.reference_bits[page] = False
