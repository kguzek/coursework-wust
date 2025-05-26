from lab3.algorithms.base import PageAllocationAlgorithm


class OPT(PageAllocationAlgorithm):
    def __init__(self, memory_size: int):
        super().__init__(memory_size)
        self.sequence: list[int] = []

    def run(self, sequence: list[int]) -> None:
        self.sequence = sequence
        super().run(sequence)

    def _process_page(self, page: int) -> None:
        current_index = len(self.history)
        if page in self.memory:
            self.page_hits += 1
            return

        self.page_faults += 1

        if len(self.memory) < self.memory_size:
            self.memory.append(page)
        else:
            future = self.sequence[current_index + 1:]
            indices = {
                p: future.index(p) if p in future else float("inf")
                for p in self.memory
            }
            evict_page = max(indices, key=indices.get)
            self.memory.remove(evict_page)
            self.memory.append(page)
