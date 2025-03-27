class Process:
    """Process class to store process information"""

    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0
        self.is_complete = False
        self.process_start_time: int | None = None
        self.completion_time: int | None = None

    # def reset(self):
    #     """Reset the process to initial state"""
    #     self.remaining_time = self.burst_time
    #     self.wait_time = 0
    #     self.is_complete = False
    #     self.process_start_time = None
    #     self.completion_time = None

    def tick(self, time: int = 1):
        """Perform a tick of the process"""
        if not self.is_complete:
            self.wait_time += time

    def complete(self, current_time: int):
        """Mark the process as complete"""
        # print(self.name, 'completed at', current_time)
        self.is_complete = True
        self.completion_time = current_time

    def process(self, current_time: int, time: int = 1):
        """Perform the process for given time"""
        if self.process_start_time is None:
            self.process_start_time = current_time
        if self.remaining_time <= time:
            self.complete(current_time + self.remaining_time)
            self.remaining_time = 0
        else:
            self.remaining_time -= time

    def get_completion_time(self):
        return self.completion_time - self.process_start_time

    def get_idle_time(self):
        return self.process_start_time - self.arrival_time

    def __lt__(self, other):
        return self.remaining_time < other.remaining_time

    def __repr__(self):
        name = self.name
        arrival = self.arrival_time
        burst = self.burst_time
        waiting = self.wait_time
        remaining = self.remaining_time
        started = self.process_start_time
        completed = self.completion_time
        time = f"completed_in={self.get_completion_time()}" if self.is_complete else f"{remaining=}"
        return f"<Process {name=} {arrival=} {burst=} {waiting=} {started=} {completed=} {time}>"
