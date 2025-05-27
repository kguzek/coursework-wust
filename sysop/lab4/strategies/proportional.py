from lab4.strategies.base import FrameAllocationStrategy


class ProportionalAllocation(FrameAllocationStrategy):
    def allocate(self, total_frames: int, processes: dict[str, list[int]]) -> dict[str, int]:
        total_requests = sum(len(seq) for seq in processes.values())
        allocations = {pid: max(1, round(len(seq) / total_requests * total_frames)) for pid, seq in processes.items()}
        while sum(allocations.values()) > total_frames:
            max_pid = max(allocations, key=allocations.get)
            if allocations[max_pid] > 1:
                allocations[max_pid] -= 1
        while sum(allocations.values()) < total_frames:
            min_pid = min(allocations, key=allocations.get)
            allocations[min_pid] += 1
        return allocations
