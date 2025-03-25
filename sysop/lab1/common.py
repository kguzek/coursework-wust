import random

from .process import Process

type SimulationResult = tuple[float, list[tuple[int, int, Process]], int | float, list[Process], int | float]
type TestCase = tuple[int, int, int, str]

DEFAULT_ITERATION_COUNT: int = 30
DEBUG_MODE = False


def get_word_file(words_filename: str = "/usr/share/dict/words"):
    with open(words_filename, 'r', encoding="utf-8") as file:
        return file.read().splitlines()


WORDS = get_word_file()


def has_incomplete_processes(processes: list[Process]):
    """Check if there are any incomplete processes"""
    return any(not process.is_complete for process in processes)


def calculate_average_completion_time(processes: list[Process]):
    """Calculate the average completion time of processes"""
    return sum(process.wait_time for process in processes) / len(processes)


def get_queued_processes(processes: list[Process], current_time: int):
    """Get the processes that have arrived in the queue and are incomplete"""
    return [
        process
        for process in processes
        if process.arrival_time <= current_time and not process.is_complete
    ]


def generate_processes(process_count: int, average_arrival_time: float, max_burst_time: int):
    """Generate random processes"""
    processes: list[Process] = []
    for name in random.sample(WORDS, process_count):
        burst_time = random.randint(1, max_burst_time)
        arrival_time = int(random.expovariate(1 / average_arrival_time))
        processes.append(Process(name, arrival_time, burst_time))
    processes.sort(key=lambda process: process.arrival_time)
    return processes
