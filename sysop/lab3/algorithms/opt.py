from lab3.algorithms.base import PageAllocationAlgorithm


class OPT(PageAllocationAlgorithm):
    def _process_page(self, page: int, current_index: int) -> None:
        if page in self.memory:
            self.page_hits += 1
            return

        self.page_faults += 1
        if len(self.memory) < self.memory_size:
            self.memory.append(page)
            return

        # Find the page in memory with the farthest next use (or no future use)
        farthest_index = -1
        page_to_replace = None
        for mem_page in self.memory:
            try:
                next_use = self.sequence.index(mem_page, current_index + 1)
            except ValueError:
                # Page not used again, perfect candidate
                page_to_replace = mem_page
                break
            if next_use > farthest_index:
                farthest_index = next_use
                page_to_replace = mem_page

        replace_idx = self.memory.index(page_to_replace)
        self.memory[replace_idx] = page
