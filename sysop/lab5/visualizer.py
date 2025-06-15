import matplotlib.pyplot as plt

from lab5.algorithms.base import ConcurrentProcessScheduler
from lab5.snapshot import ProcessorSnapshot, SchedulerSnapshot


def display_results(algorithm: ConcurrentProcessScheduler) -> None:
    result: list[tuple[list[ProcessorSnapshot], SchedulerSnapshot]] = algorithm.statistics

    # Extract time series data
    load_averages = []
    load_standard_deviations = []
    total_queries = []
    total_delegated_processes = []

    for _, scheduler_snapshot in result:
        load_averages.append(scheduler_snapshot.load_average)
        load_standard_deviations.append(scheduler_snapshot.load_standard_deviation)
        total_queries.append(scheduler_snapshot.total_load_queries)
        total_delegated_processes.append(scheduler_snapshot.total_delegated_processes)

    # Setup figure with 4 subplots
    fig, axs = plt.subplots(4, 1, figsize=(16, 8), sharex=True)
    fig.suptitle(f"Metrics for {algorithm}", fontsize=16)

    line_width = 1.5

    # Plot 1: Load Average
    # axs[0].plot(load_averages, color='blue', linewidth=line_width)
    axs[0].errorbar(
        x=range(len(load_averages)),
        y=load_averages,
        yerr=load_standard_deviations,
        color='blue',
        ecolor='lightblue',  # colour of error bars
        elinewidth=0.5,  # thickness of error bars
        capsize=1,  # length of error bar caps
        linewidth=line_width  # line width of the average line
    )
    axs[0].set_ylabel('Load Average (%)')
    axs[0].grid(True)

    # Plot 2: Load Standard Deviation
    axs[1].plot(load_standard_deviations, color='green', linewidth=line_width)
    axs[1].set_ylabel('Load Std Dev (%)')
    axs[1].grid(True)

    # Plot 3: Total Load Queries
    axs[2].plot(total_queries, color='red', linewidth=line_width)
    axs[2].set_ylabel('Total Load Queries')
    axs[2].grid(True)

    # Plot 4: Total Delegated Processes
    axs[3].plot(total_delegated_processes, color='purple', linewidth=line_width)
    axs[3].set_ylabel('Total Delegated Processes')
    axs[3].set_xlabel('Timestep')
    axs[3].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
