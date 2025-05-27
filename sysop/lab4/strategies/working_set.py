from lab4.strategies.base import FrameAllocationStrategy, normalize_allocations

delta_t = 50


class WorkingSetModel(FrameAllocationStrategy):
    def allocate(self, total_frames: int, processes: dict[str, list[int]]) -> dict[str, int]:
        working_sets = {
            pid: len(set(seq[-delta_t:] if len(seq) >= delta_t else seq))
            for pid, seq in processes.items()
        }
        total_ws = sum(working_sets.values())
        allocations = {
            pid: max(1, round(ws / total_ws * total_frames))
            for pid, ws in working_sets.items()
        }
        return normalize_allocations(allocations, total_frames)
