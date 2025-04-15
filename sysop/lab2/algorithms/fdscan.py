from lab2.algorithms.scan import Scan
from lab2.algorithms.strategy import DeadlineStrategy
from lab2.request import DiskAccessRequest


class FDScan(DeadlineStrategy, Scan):
    def tick_chamber(self):
        self.tick_chamber_simple()

    def tick_chamber_with_deadline(self):
        self.tick_chamber_simple()

    def select_target_request_with_deadline(self,
                                            queue_with_deadlines: list[DiskAccessRequest]) -> DiskAccessRequest | None:
        queue = [request for request in queue_with_deadlines if
                 abs(request.chamber - self.current_chamber) <= request.deadline]
        return None if len(queue) == 0 else queue[0]
