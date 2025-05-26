import random
from typing import NamedTuple, List, Generator

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


class PageRequestSequence:
    def __init__(self, config: SimulationConfig, seed: int | None = None):
        self.config = config
        if seed is not None:
            random.seed(seed)
        self.sequence: List[int] = self._generate_sequence()

    def _generate_sequence(self) -> List[int]:
        return [random.randint(0, self.config.num_pages - 1)
                for _ in range(self.config.request_count)]

    def __iter__(self) -> Generator[int, None, None]:
        yield from self.sequence

    def __repr__(self) -> str:
        return f"<PageRequestSequence {self.sequence[:10]}{'...' if len(self.sequence) > 10 else ''}>"


class AlgorithmTestCase(NamedTuple):
    config: SimulationConfig
    sequence: PageRequestSequence
    algorithm: PageAllocationAlgorithm


def generate_simulation_case(seed: int | None = None) -> List[AlgorithmTestCase]:
    """
    Generate a deeper simulation configuration to better stress test algorithm differences.
    """
    if seed is not None:
        random.seed(seed)

    # More varied and higher scale
    num_pages = random.choice([20, 50, 100])
    memory_ratios = [0.1, 0.25, 0.5]  # memory as % of num_pages
    memory_size = int(num_pages * random.choice(memory_ratios))
    memory_size = max(2, min(memory_size, num_pages))

    request_count = random.choice([200, 500, 1000])  # longer sequences to observe long-term behavior

    config = SimulationConfig(
        num_pages=num_pages,
        memory_size=memory_size,
        request_count=request_count
    )
    sequence = PageRequestSequence(config=config, seed=seed)

    return [
        AlgorithmTestCase(config=config, sequence=sequence, algorithm=algorithm(config.memory_size))
        for algorithm in [ALRU, FIFO, LRU, OPT, Rand]
    ]
