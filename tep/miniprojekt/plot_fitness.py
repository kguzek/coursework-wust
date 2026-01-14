#!/usr/bin/env python3
"""
Plot fitness progress from genetic algorithm optimization
"""

import sys

import matplotlib.pyplot as plt
import pandas as pd


def plot_fitness(filename):
    """
    Read CSV file and plot fitness progression over iterations

    Args:
        filename: Path to CSV file with iteration,fitness columns
    """
    try:
        data = pd.read_csv(filename)

        if "iteration" not in data.columns or "fitness" not in data.columns:
            print("Error: CSV file must contain 'iteration' and 'fitness' columns")
            return

        plt.figure(figsize=(12, 6))

        plt.plot(data["iteration"], data["fitness"], linewidth=1.5, color="#2E86AB")

        plt.xlabel("Iteration", fontsize=12)
        plt.ylabel("Fitness", fontsize=12)
        plt.title("Genetic Algorithm Fitness Progress", fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3, linestyle="--")

        best_fitness = data["fitness"].max()
        best_iteration = data.loc[data["fitness"].idxmax(), "iteration"]

        plt.axhline(
            y=best_fitness,
            color="#A23B72",
            linestyle="--",
            linewidth=1,
            label=f"Best: {best_fitness:.2f} at iteration {int(best_iteration)}",
        )

        plt.legend(loc="lower right", fontsize=10)

        plt.tight_layout()

        output_filename = filename.replace(".csv", "_plot.png")
        plt.savefig(output_filename, dpi=300, bbox_inches="tight")
        print(f"Plot saved to: {output_filename}")

        plt.show()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 plot_fitness.py <fitness_csv_file>")
        print("Example: python3 plot_fitness.py ORTEC-n323-k21_fitness.csv")
        sys.exit(1)

    filename = sys.argv[1]
    plot_fitness(filename)


if __name__ == "__main__":
    main()
