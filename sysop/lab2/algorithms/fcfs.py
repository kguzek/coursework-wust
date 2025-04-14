from lab2.algorithms.base import DiskAccessAlgorithm
from lab2.request import DiskAccessRequest


class FCFS(DiskAccessAlgorithm):
    def tick_chamber(self):
        if self.current_request is None or self.current_request.chamber == self.current_chamber:
            return
        if self.current_request.chamber > self.current_chamber:
            self.next_chamber()
        else:
            self.previous_chamber()

    def select_target_request(self) -> DiskAccessRequest | None:
        return self.queue[0] if len(self.queue) > 0 else None
