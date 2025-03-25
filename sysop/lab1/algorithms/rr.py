from .base import Algorithm


class RR(Algorithm):
    """Round Robin (RR) scheduling algorithm"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_process_index = 0

    def select_current_process(self):
        if len(self.queue) == 0:
            return None
        if self.previous_process is None or len(self.queue) == 1:
            self.previous_process_index = 0
            return self.queue[self.previous_process_index]
        next_process_index = (self.previous_process_index + 1) \
            if self.previous_process in self.queue \
            else self.previous_process_index
        self.previous_process_index = next_process_index % len(self.queue)
        return self.queue[self.previous_process_index]
