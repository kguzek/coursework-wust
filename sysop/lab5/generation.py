import random

from lab5.process import Process
from lab5.processor import Processor

PROCESS_COUNT_MIN = 1000
PROCESS_COUNT_MAX = 10000

PROCESS_LOAD_MIN = 1
PROCESS_LOAD_MAX = 20

ARRIVAL_TIME_MULTIPLIER = 1

PROCESS_BURST_MIN = 200
PROCESS_BURST_MAX = 1000

PROCESSOR_COUNT_MIN = 50
PROCESSOR_COUNT_MAX = 100


def generate_process(index: int) -> Process:
    load_burden: int = random.randint(PROCESS_LOAD_MIN, PROCESS_LOAD_MAX)
    arrival_time: int = int(random.expovariate(1.0 / (index * ARRIVAL_TIME_MULTIPLIER)))
    burst_time: int = random.randrange(PROCESS_BURST_MIN, PROCESS_BURST_MAX)
    return Process(load_burden, arrival_time, burst_time)


def generate_processor() -> Processor:
    process_count: int = random.randint(PROCESS_COUNT_MIN, PROCESS_COUNT_MAX)
    processes = [generate_process(index) for index in range(1, process_count + 1)]
    return Processor(processes)


def generate_processor_count() -> int:
    return random.randint(PROCESSOR_COUNT_MIN, PROCESSOR_COUNT_MAX)
