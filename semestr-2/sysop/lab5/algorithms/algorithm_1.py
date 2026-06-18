from lab5.algorithms.base import ConcurrentProcessScheduler
from lab5.process import Process
from lab5.processor import Processor


class Algorithm1(ConcurrentProcessScheduler):
    def __init__(self, processors: list[Processor], processor_load_threshold: int, max_delegation_attempts: int):
        super().__init__(processors, processor_load_threshold)
        self.max_delegation_attempts = max_delegation_attempts

    def select_target_processor(self, initial_processor: Processor, process: Process) -> tuple[Processor | None, int]:
        candidate_processors = self.get_candidate_processors(initial_processor)
        for _ in range(self.max_delegation_attempts):
            if len(candidate_processors) == 0:
                break
            candidate_processor = self.select_random_processor(candidate_processors)
            load = candidate_processor.query_load()
            if load < self.processor_load_threshold:
                return candidate_processor, load
        if initial_processor.would_overload(process):
            return None, 100
        return initial_processor, 0
