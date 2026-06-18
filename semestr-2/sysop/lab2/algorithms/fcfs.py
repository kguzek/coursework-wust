from lab2.algorithms.base import DiskAccessAlgorithm
from lab2.request import DiskAccessRequest


class FCFS(DiskAccessAlgorithm):
    def tick_chamber(self):
        self.tick_chamber_simple()

    def select_target_request(self) -> DiskAccessRequest | None:
        return self.queue[0] if len(self.queue) > 0 else None
