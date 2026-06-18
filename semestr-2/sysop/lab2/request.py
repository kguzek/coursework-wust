class DiskAccessRequest:
    def __init__(self, chamber: int, arrival_time: int, deadline: int = -1):
        self.chamber: int = chamber
        self.arrival_time: int = arrival_time
        self.deadline: int = deadline
        self.time_completed: int | None = None
        self.failed: bool = False

    def tick(self, current_time: int):
        if current_time < self.arrival_time:
            return
        if self.failed or self.deadline == -1 or self.time_completed is not None:
            return
        self.deadline -= 1
        if self.deadline <= 0:
            self.failed = True

    def is_pending(self) -> bool:
        return self.time_completed is None and not self.failed

    def complete(self, current_time: int):
        self.time_completed = current_time

    def __repr__(self):
        arrival_time = self.arrival_time
        chamber = self.chamber
        status = "failed" if self.failed \
            else ("idle" if self.deadline == -1 else f"T-{self.deadline}") \
            if self.time_completed is None else "completed"
        return f"Request({arrival_time=}, {chamber=}, {status=})"
