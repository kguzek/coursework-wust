from abc import abstractmethod

from lab2.algorithms.base import DiskAccessAlgorithm
from lab2.request import DiskAccessRequest


class DeadlineStrategy(DiskAccessAlgorithm):
    def has_pending_deadlines(self):
        return any(request.deadline > 0 for request in self.queue)

    @abstractmethod
    def tick_chamber_with_deadline(self) -> None:
        """Ticks to the request with a passing deadline."""

    @abstractmethod
    def select_target_request_with_deadline(self, requests_with_deadline: list[
        DiskAccessRequest]) -> DiskAccessRequest | None:
        """Selects the target request based on its deadline."""

    def tick_chamber(self):
        if self.current_request is None:
            super().tick_chamber()
        else:
            self.tick_chamber_with_deadline()

    def select_target_request(self) -> DiskAccessRequest | None:
        self.scan = True
        has_deadlines = self.has_pending_deadlines()
        if has_deadlines:
            requests = sorted([request for request in self.queue if request.deadline >= 0], key=lambda r: r.deadline)
            return self.select_target_request_with_deadline(requests)
        return super().select_target_request()
