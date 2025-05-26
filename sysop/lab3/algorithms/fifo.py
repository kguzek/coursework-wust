from collections import deque

from lab3.algorithms.base import PageAllocationAlgorithm


class FIFO(PageAllocationAlgorithm):
    def __init__(self, memory_size: int):
        super().__init__(memory_size)
        self.queue = deque()

    def _process_page(self, page: int) -> None:
        if page in self.memory:
            self.page_hits += 1
            return

        self.page_faults += 1

        if len(self.memory) < self.memory_size:
            self.memory.append(page)
            self.queue.append(page)
        else:
            old_page = self.queue.popleft()
            self.memory.remove(old_page)
            self.memory.append(page)
            self.queue.append(page)
