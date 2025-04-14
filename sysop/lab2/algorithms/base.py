from abc import abstractmethod
from copy import deepcopy

from lab2.request import DiskAccessRequest


class DiskAccessAlgorithm:
    # pylint: disable=too-many-arguments
    def __init__(self, requests: list[DiskAccessRequest], scan: bool = False, cycled: bool = False, *,
                 current_chamber: int = 0, num_chambers: int = 100):
        self.requests = deepcopy(requests)
        self.queue: list[DiskAccessRequest] = []
        self.current_time: int = 0
        self.current_request: DiskAccessRequest | None = None
        self.current_chamber: int = current_chamber
        self.scan: bool = scan
        self.cycled: bool = cycled
        self.num_chambers: int = num_chambers

    def has_pending_requests(self):
        return any(request.is_pending() for request in self.requests)

    def next_chamber(self):
        if self.current_chamber >= self.num_chambers:
            if self.cycled:
                self.current_chamber = 1
            else:
                self.previous_chamber()
        else:
            self.current_chamber += 1

    def previous_chamber(self):
        if self.current_chamber <= 1:
            if self.cycled:
                self.current_chamber = self.num_chambers
            else:
                self.next_chamber()
        else:
            self.current_chamber -= 1

    @abstractmethod
    def select_target_request(self) -> DiskAccessRequest | None:
        """Selects the request that the algorithm should currently aim to process."""

    @abstractmethod
    def tick_chamber(self):
        """Progresses the current chamber pointer."""

    def generate_queue(self):
        return [request for request in self.requests if
                request.arrival_time <= self.current_time and request.is_pending()]

    def tick(self) -> None:
        if self.current_request is None:
            self.queue = self.generate_queue()
            self.queue.sort(key=lambda queued_request: queued_request.arrival_time)
            self.current_request = self.select_target_request()
        self.tick_chamber()
        if self.current_request is not None:
            if self.current_chamber == self.current_request.chamber:
                # extension point - assuming requests are handled instantly
                self.current_request.complete(self.current_time)
                self.current_request = None
        for request in self.requests:
            request.tick(self.current_time)
        self.current_time += 1
