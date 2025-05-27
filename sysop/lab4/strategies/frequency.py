from lab4.strategies.base import FrameAllocationStrategy, normalize_allocations


class PageFaultFrequency(FrameAllocationStrategy):
    def allocate(self, total_frames: int, processes: dict[str, list[int]]) -> dict[str, int]:
        simulated_faults = {
            pid: len(set(seq[:min(50, len(seq))]))  # mockup simulation of the first 50 requests
            for pid, seq in processes.items()
        }
        total_faults = sum(simulated_faults.values())
        allocations = {
            pid: max(1, round(faults / total_faults * total_frames))
            for pid, faults in simulated_faults.items()
        }
        return normalize_allocations(allocations, total_frames)
