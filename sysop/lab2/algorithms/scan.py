from lab2.algorithms.base import DiskAccessAlgorithm
from lab2.request import DiskAccessRequest


class Scan(DiskAccessAlgorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, scan=True)
        self.increasing = True

    def tick_chamber(self):
        if self.increasing:
            hit_boundary = self.next_chamber()
        else:
            hit_boundary = self.previous_chamber()
        if hit_boundary:
            self.increasing = not self.increasing

    def select_target_request(self) -> DiskAccessRequest | None:
        return None
