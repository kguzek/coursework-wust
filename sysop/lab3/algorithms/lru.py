from lab3.algorithms.base import PageAllocationAlgorithm


class LRU(PageAllocationAlgorithm):
    def __init__(self, memory_size: int):
        super().__init__(memory_size)
        self.recently_used: list[int] = []

    def _process_page_hit(self, page: int) -> None:
        super()._process_page_hit(page)
        self.recently_used.remove(page)
        self.recently_used.append(page)

    def _process_page(self, page: int, *args) -> None:
        if len(self.memory) < self.memory_size:
            self.memory.append(page)
            self.recently_used.append(page)
        else:
            lru_page = self.recently_used.pop(0)
            self.memory.remove(lru_page)
            self.memory.append(page)
            self.recently_used.append(page)
