from .base import Algorithm


class RR(Algorithm):
    """Round Robin (RR) scheduling algorithm"""

    def select_current_process(self):
        if len(self.queue) == 0:
            return None
        if self.previous_process_id is None:
            return self.queue[0]
        if len(self.queue) == 1:
            return self.queue[0]
        for process in self.queue:
            if id(process) != self.previous_process_id:
                return process
        return None
