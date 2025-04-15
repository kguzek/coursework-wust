import sys

from lab2.simulation import run_simulation, run_simulation_with_deadlines


def main():
    if "-s" in sys.argv:
        run_simulation_with_deadlines()
    else:
        run_simulation()


if __name__ == "__main__":
    main()
