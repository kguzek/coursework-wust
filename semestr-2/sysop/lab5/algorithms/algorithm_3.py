import math

from lab5.algorithms.algorithm_2 import Algorithm2
from lab5.process import Process
from lab5.processor import Processor

PROCESS_BALANCING_PROPORTION = 0.1


class Algorithm3(Algorithm2):
    def __init__(self, processors: list[Processor], processor_load_threshold: int, processor_balancing_threshold: int):
        super().__init__(processors, processor_load_threshold)
        self.processor_balancing_threshold = processor_balancing_threshold

    def perform_load_balancing(self, load: int, processor: Processor) -> None:
        """Makes the processor take on processes from other CPUs which are under more load."""
        other_processors = self.get_candidate_processors(processor)
        for other_processor in other_processors:
            other_load = other_processor.query_load()
            if load > self.processor_balancing_threshold:
                break
            if other_load > self.processor_load_threshold:
                other_total_processes = len(other_processor.active_processes)
                processes_to_take_over = math.floor(PROCESS_BALANCING_PROPORTION * other_total_processes)
                for _ in range(processes_to_take_over):
                    process = other_processor.active_processes[0]
                    if processor.would_overload(process):
                        break
                    other_processor.active_processes.pop(0)
                    other_processor.processes_delegated += 1
                    processor.assign_process(process)
                    load += process.load_burden

    def select_target_processor(self, initial_processor: Processor, process: Process) -> tuple[Processor, int]:
        selected_processor, load = super().select_target_processor(initial_processor, process)
        self.perform_load_balancing(load, initial_processor)
        return selected_processor, load
