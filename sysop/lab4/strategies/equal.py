from typing import Dict, List

from lab4.strategies.base import FrameAllocationStrategy


class EqualAllocation(FrameAllocationStrategy):
    def allocate(self, total_frames: int, processes: Dict[str, List[int]]) -> Dict[str, int]:
        num_procs = len(processes)
        base = total_frames // num_procs
        rem = total_frames % num_procs
        allocations = {pid: base for pid in processes}
        for pid in list(processes.keys())[:rem]:
            allocations[pid] += 1
        return allocations
