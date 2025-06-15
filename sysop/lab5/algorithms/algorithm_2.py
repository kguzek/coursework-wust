from lab5.algorithms.base import ConcurrentProcessScheduler
from lab5.process import Process
from lab5.processor import Processor


class Algorithm2(ConcurrentProcessScheduler):

    def select_target_processor(self, initial_processor: Processor, process: Process) -> tuple[Processor | None, int]:
        load = initial_processor.query_load()
        if load < self.processor_load_threshold:
            return initial_processor, load
        candidate_processors = self.get_candidate_processors(initial_processor)
        while len(candidate_processors) > 0:
            candidate_processor = self.select_random_processor(candidate_processors)
            if candidate_processor.query_load() < self.processor_load_threshold:
                return candidate_processor, load
        return None, 100
