from .base import Algorithm


class SRTF(Algorithm):
    """Shortest Remaining Time First (SRTF) scheduling algorithm"""

    def select_current_process(self):
        self.queue.sort(key=lambda x: x.remaining_time)
        return self.queue[0] if len(self.queue) > 0 else None


3
