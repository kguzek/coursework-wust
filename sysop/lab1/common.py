from .process import Process


def has_incomplete_processes(processes: list[Process]):
    """Check if there are any incomplete processes"""
    return any(not process.is_complete for process in processes)


def calculate_average_completion_time(processes: list[Process]):
    """Calculate the average completion time of processes"""
    return sum(process.wait_time for process in processes) / len(processes)


def get_queued_processes(processes: list[Process], current_time: int):
    """Get the processes that have arrived in the queue and are incomplete"""
    return [
        process
        for process in processes
        if process.arrival_time <= current_time and not process.is_complete
    ]


def reset_processes(processes: list[Process]):
    """Resets the processes to their initial state and sorts them by arrival time"""
    for process in processes:
        process.reset()
    processes.sort(key=lambda x: x.arrival_time)
