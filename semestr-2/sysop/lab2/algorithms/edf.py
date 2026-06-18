from lab2.algorithms.scan import Scan
from lab2.algorithms.strategy import DeadlineStrategy
from lab2.request import DiskAccessRequest


class EDF(DeadlineStrategy, Scan):
    def tick_chamber_with_deadline(self) -> None:
        self.tick_chamber_simple()

    def select_target_request_with_deadline(self, requests_with_deadline) -> DiskAccessRequest | None:
        self.scan = False
        return None if len(requests_with_deadline) == 0 else requests_with_deadline[0]
