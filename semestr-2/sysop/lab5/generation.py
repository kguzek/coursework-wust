import random

from lab5.process import Process
from lab5.processor import Processor

PROCESS_COUNT_MIN = 100
PROCESS_COUNT_MAX = 1000

PROCESS_LOAD_MIN = 1
PROCESS_LOAD_MAX = 20

PROCESS_BURST_MIN = 1
PROCESS_BURST_MAX = 20

PROCESSOR_COUNT_MIN = 50
PROCESSOR_COUNT_MAX = 100


def generate_process() -> Process:
    load_burden: int = random.randint(PROCESS_LOAD_MIN, PROCESS_LOAD_MAX)
    arrival_time: int = random.randrange(PROCESS_COUNT_MAX)
    burst_time: int = random.randrange(PROCESS_BURST_MIN, PROCESS_BURST_MAX)
    return Process(load_burden, arrival_time, burst_time)


def generate_processor() -> Processor:
    process_count: int = random.randint(PROCESS_COUNT_MIN, PROCESS_COUNT_MAX)
    processes = [generate_process() for _ in range(process_count)]
    return Processor(processes)


def generate_processor_count() -> int:
    return random.randint(PROCESSOR_COUNT_MIN, PROCESSOR_COUNT_MAX)
