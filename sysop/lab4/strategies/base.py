from abc import ABC, abstractmethod
from typing import Dict, List


def normalize_allocations(allocations, total_frames):
    while sum(allocations.values()) > total_frames:
        max_pid = max(allocations, key=allocations.get)
        if allocations[max_pid] > 1:
            allocations[max_pid] -= 1
        else:
            break
    while sum(allocations.values()) < total_frames:
        min_pid = min(allocations, key=allocations.get)
        allocations[min_pid] += 1
    return allocations


class FrameAllocationStrategy(ABC):
    @abstractmethod
    def allocate(self, total_frames: int, processes: Dict[str, List[int]]) -> Dict[str, int]:
        pass
