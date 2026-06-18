from lab2.algorithms.base import DiskAccessAlgorithm
from lab2.request import DiskAccessRequest


class SSTF(DiskAccessAlgorithm):
    def tick_chamber(self):
        self.tick_chamber_simple()

    def select_target_request(self) -> DiskAccessRequest | None:
        self.queue.sort(key=lambda request: abs(request.chamber - self.current_chamber))
        return self.queue[0] if len(self.queue) > 0 else None
