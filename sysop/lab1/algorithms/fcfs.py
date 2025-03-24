from .base import Algorithm


class FCFS(Algorithm):
    """First-Come, First-Served (FCFS) scheduling algorithm"""

    def select_current_process(self):
        if len(self.queue) == 0:
            return None
        first_process = self.queue[0]
        sorted_queue = [process for process in self.queue if process.remaining_time == first_process.remaining_time]
        return sorted_queue[0]
