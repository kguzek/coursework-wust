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

    def next_chamber(self) -> bool:
        hit_boundary = self.current_chamber >= self.num_chambers
        if hit_boundary:
            if self.cycled:
                self.current_chamber = 1
            else:
                self.previous_chamber()
        else:
            self.current_chamber += 1
        return hit_boundary

    def previous_chamber(self) -> bool:
        hit_boundary = self.current_chamber <= 1
        if hit_boundary:
            if self.cycled:
                self.current_chamber = self.num_chambers
            else:
                self.next_chamber()
        else:
            self.current_chamber -= 1
        return hit_boundary

    @abstractmethod
    def select_target_request(self) -> DiskAccessRequest | None:
        """Selects the request that the algorithm should currently aim to process."""

    def tick_chamber_simple(self):
        """Performs a simple chamber tick attempting to reach the currently active request."""
        if self.current_request is None or self.current_request.chamber == self.current_chamber:
            return
        if self.current_request.chamber > self.current_chamber:
            self.next_chamber()
        else:
            self.previous_chamber()

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
        requests_to_complete = self.queue if self.scan else [self.current_request]
        for request in requests_to_complete:
            if request is not None and request.chamber == self.current_chamber:
                # extension point - assuming requests are handled instantly
                request.complete(self.current_time)
                self.current_request = None
        for request in self.requests:
            request.tick(self.current_time)
        self.current_time += 1
