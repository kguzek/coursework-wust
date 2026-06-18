import random

from lab3.algorithms.base import PageAllocationAlgorithm


class Rand(PageAllocationAlgorithm):
    def _process_page(self, page: int, *unused_args) -> None:
        if len(self.memory) < self.memory_size:
            self.memory.append(page)
        else:
            evict_index = random.randint(0, self.memory_size - 1)
            self.memory[evict_index] = page
