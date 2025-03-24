from .base import Algorithm


class SJF(Algorithm):
    """Shortest Job First (SJF) scheduling algorithm"""

    def select_current_process(self):
        self.queue.sort(key=lambda x: x.burst_time)
        return (
            self.current_process
            if self.current_process is not None
            else self.queue[0] if len(self.queue) > 0 else None
        )
