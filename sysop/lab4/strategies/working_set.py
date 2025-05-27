from typing import Dict, List

from lab4.strategies.base import FrameAllocationStrategy, normalize_allocations


class WorkingSetModel(FrameAllocationStrategy):
    def allocate(self, total_frames: int, processes: Dict[str, List[int]]) -> Dict[str, int]:
        working_sets = {
            pid: len(set(seq[-50:])) if len(seq) >= 50 else len(set(seq))
            for pid, seq in processes.items()
        }
        total_ws = sum(working_sets.values())
        allocations = {
            pid: max(1, round(ws / total_ws * total_frames))
            for pid, ws in working_sets.items()
        }
        return normalize_allocations(allocations, total_frames)
