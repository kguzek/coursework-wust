from dataclasses import dataclass
from typing import List

from lab3.preparation import generate_simulation_case, AlgorithmTestCase


@dataclass
class SimulationResult:
    algorithm: str
    page_faults: int
    page_hits: int
    requests: int
    memory: int
    pages: int


def run_test_case(test_case: AlgorithmTestCase) -> SimulationResult:
    test_case.algorithm.reset()
    test_case.algorithm.run(list(test_case.sequence))

    stats = test_case.algorithm.stats()
    return SimulationResult(
        algorithm=test_case.algorithm.__class__.__name__,
        page_faults=stats["page_faults"],
        page_hits=stats["page_hits"],
        requests=test_case.config.request_count,
        memory=test_case.config.memory_size,
        pages=test_case.config.num_pages
    )


def run_all_simulations() -> List[SimulationResult]:
    cases = generate_simulation_case()
    return [run_test_case(case) for case in cases]
