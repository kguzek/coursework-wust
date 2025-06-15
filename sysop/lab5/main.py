from lab5.algorithms.algorithm_1 import Algorithm1
from lab5.algorithms.algorithm_2 import Algorithm2
from lab5.algorithms.algorithm_3 import Algorithm3
from lab5.generation import generate_processor_count, generate_processor
from lab5.visualizer import display_results


def main():
    p: int = 80  # Load ceiling for passively accepting queued processes
    r: int = 60  # Load ceiling for actively handling other processes
    z: int = 10  # Maximum number of random processor selections per tick
    n: int | None = None  # Number of processors

    if n is None:
        # `None` losuje ilość procesorów w przedziale [50,100]
        n = generate_processor_count()

    processors = [generate_processor() for _ in range(n)]

    algorithms = [
        Algorithm1(processors, processor_load_threshold=p, max_delegation_attempts=z),
        Algorithm2(processors, processor_load_threshold=p),
        Algorithm3(processors, processor_load_threshold=p, processor_balancing_threshold=r),
    ]

    print("Running simulation with", n, "processors:")

    for algorithm in algorithms:
        print("Running", algorithm, "...")
        algorithm.run()

    print("Rendering results!")

    for algorithm in algorithms:
        display_results(algorithm)


if __name__ == "__main__":
    main()
