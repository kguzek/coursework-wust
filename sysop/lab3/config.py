import random
from typing import List, NamedTuple

from lab3.algorithms.alru import ALRU
from lab3.algorithms.base import PageAllocationAlgorithm
from lab3.algorithms.fifo import FIFO
from lab3.algorithms.lru import LRU
from lab3.algorithms.opt import OPT
from lab3.algorithms.rand import Rand


class SimulationConfig(NamedTuple):
    num_pages: int
    memory_size: int
    request_count: int


def generate_page_request_sequence(config: SimulationConfig, seed: int | None = None) -> List[int]:
    if seed is not None:
        random.seed(seed)
    return [random.randint(0, config.num_pages - 1) for _ in range(config.request_count)]


class AlgorithmTestCase(NamedTuple):
    config: SimulationConfig
    sequence: List[int]
    algorithm: PageAllocationAlgorithm


def generate_simulation_case(seed: int | None = None) -> List[AlgorithmTestCase]:
    if seed is not None:
        random.seed(seed)

    num_pages = random.choice([20, 50, 100])
    memory_ratios = [0.1, 0.25, 0.5]  # memory as % of num_pages
    memory_size = int(num_pages * random.choice(memory_ratios))
    memory_size = max(2, min(memory_size, num_pages))

    request_count = random.choice([200, 500, 1000])

    config = SimulationConfig(
        num_pages=num_pages,
        memory_size=memory_size,
        request_count=request_count
    )
    sequence = generate_page_request_sequence(config, seed=seed)

    return [
        AlgorithmTestCase(config=config, sequence=sequence, algorithm=algorithm(config.memory_size))
        for algorithm in [ALRU, FIFO, LRU, OPT, Rand]
    ]
