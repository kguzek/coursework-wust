from typing import Self


class Process:
    def __init__(self, load_burden: int, arrival_time: int, burst_time: int):
        self.load_burden: int = load_burden
        self.arrival_time: int = arrival_time
        self.burst_time: int = 0
        self.completed = False

    def is_running(self) -> bool:
        return not self.completed

    def is_active(self, current_time: int) -> bool:
        return self.is_running() and self.arrival_time <= current_time

    def tick(self):
        if self.burst_time > 1:
            self.burst_time -= 1
        else:
            self.burst_time = 0
            self.completed = True

    def __repr__(self):
        return f"Process(load_burden={self.load_burden}, arrival_time={self.arrival_time}, burst_time={self.burst_time})"

    def copy(self) -> Self:
        return Process(load_burden=self.load_burden, arrival_time=self.arrival_time, burst_time=self.burst_time)
