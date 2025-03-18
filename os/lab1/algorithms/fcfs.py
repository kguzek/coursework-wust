from .base import Algorithm


class FCFS(Algorithm):
    """First-Come, First-Served (FCFS) scheduling algorithm"""

    def select_current_process(self):
        return self.queue[0] if len(self.queue) > 0 else None
