import random
from typing import NamedTuple

from lab3.algorithms.base import PageAllocationAlgorithm


class SimulationConfig(NamedTuple):
    num_pages: int
    memory_size: int
    request_count: int


def generate_page_request_sequence(config: SimulationConfig, seed: int | None = None) -> list[int]:
    if seed is not None:
        random.seed(seed)
    return [random.randint(0, config.num_pages - 1) for _ in range(config.request_count)]


class AlgorithmTestCase(NamedTuple):
    config: SimulationConfig
    sequence: list[int]
    algorithm: PageAllocationAlgorithm


def generate_simulation_config(seed: int | None = None, request_count_min: int = 10_000,
                               request_count_max: int = 20_000) -> SimulationConfig:
    if seed is not None:
        random.seed(seed)

    num_pages = random.choice([20, 50, 100])
    memory_ratios = [0.1, 0.25, 0.5]  # memory as % of num_pages
    memory_size = int(num_pages * random.choice(memory_ratios))
    memory_size = max(2, min(memory_size, num_pages))
    request_count = random.randint(request_count_min, request_count_max)

    return SimulationConfig(
        num_pages=num_pages,
        memory_size=memory_size,
        request_count=request_count
    )
