from dataclasses import dataclass
from typing import List

from lab3.config import generate_simulation_case, AlgorithmTestCase


@dataclass
class SimulationResult:
    algorithm: str
    page_faults: int
    page_hits: int
    requests: int
    memory: int
    pages: int
    thrashing_events: int = 0
    locality_rate: float = 0.0
    average_pff: float = 0.0


def run_test_case(test_case: AlgorithmTestCase) -> SimulationResult:
    algo = test_case.algorithm
    algo.reset()
    algo.run(list(test_case.sequence))

    stats = algo.stats()
    return SimulationResult(
        algorithm=algo.__class__.__name__,
        page_faults=stats["page_faults"],
        page_hits=stats["page_hits"],
        requests=test_case.config.request_count,
        memory=test_case.config.memory_size,
        pages=test_case.config.num_pages,
        thrashing_events=stats.get("thrashing_events", 0),
        locality_rate=stats.get("locality_rate", 0),
        average_pff=stats.get("average_pff", 0),
    )


def run_all_simulations() -> List[SimulationResult]:
    cases = generate_simulation_case()
    return [run_test_case(case) for case in cases]
