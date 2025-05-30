from lab4.strategies.base import FrameAllocationStrategy, normalize_allocations

DELTA_T = 50


class WorkingSetModel(FrameAllocationStrategy):
    def allocate(self, total_frames: int, processes: dict[str, list[int]]) -> dict[str, int]:
        working_sets = {
            pid: len(set(seq[-DELTA_T:] if len(seq) >= DELTA_T else seq))
            for pid, seq in processes.items()
        }
        total_ws = sum(working_sets.values())
        allocations = {
            pid: max(1, round(ws / total_ws * total_frames))
            for pid, ws in working_sets.items()
        }
        return normalize_allocations(allocations, total_frames)
