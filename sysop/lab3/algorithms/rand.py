import random

from lab3.algorithms.base import PageAllocationAlgorithm


class Rand(PageAllocationAlgorithm):
    def _process_page(self, page: int) -> None:
        if page in self.memory:
            self.page_hits += 1
            return

        self.page_faults += 1

        if len(self.memory) < self.memory_size:
            self.memory.append(page)
        else:
            evict_index = random.randint(0, self.memory_size - 1)
            self.memory[evict_index] = page
