class Process:
    """Process class to store process information"""

    def __init__(self, arrival_time, burst_time):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.wait_time = 0
        self.complete = False

    def reset(self):
        """Reset the process to initial state"""
        self.remaining_time = self.burst_time
        self.wait_time = 0
        self.complete = False

    def tick(self, time=1):
        """Perform a tick of the process"""
        if not self.complete:
            self.wait_time += time

    def process(self, time=1):
        """Perform the process for given time"""
        if self.remaining_time <= time:
            self.remaining_time = 0
            self.complete = True
        else:
            self.remaining_time -= time

    def __lt__(self, other):
        return self.remaining_time < other.remaining_time
