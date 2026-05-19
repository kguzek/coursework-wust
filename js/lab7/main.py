from __future__ import annotations

import logging

from implementation import (
    PasswordGenerator,
    acronym,
    atleast,
    atmost,
    exists,
    fibonacci,
    flatten,
    forall,
    group_anagrams,
    log,
    make_alpha_dict,
    make_generator,
    make_generator_mem,
    median,
    sqrt_newton,
)


@log(logging.INFO)
def add(a: int, b: int) -> int:
    return a + b


@log(logging.DEBUG)
class DemoClass:
    def __init__(self, name: str) -> None:
        self.name = name

    def label(self) -> str:
        return self.name


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def show_task_1_examples() -> None:
    print("Task 1 examples")
    print(acronym(["Zaklad", "Ubezpieczen", "Spolecznych"]))
    print(median([1, 1, 19, 2, 3, 4, 4, 5, 1]))
    print(round(sqrt_newton(3, epsilon=0.1), 2))
    print(make_alpha_dict("on i ona"))
    print(flatten([1, [2, 3], [[4, 5], 6]]))
    print(group_anagrams(["kot", "tok", "pies", "kep", "pek"]))


def show_task_2_examples() -> None:
    print("\nTask 2 examples")
    data = [1, 2, 3, 4, 5]
    print(forall(lambda value: value > 0, data))
    print(exists(lambda value: value % 2 == 0, data))
    print(atleast(2, lambda value: value > 3, data))
    print(atmost(3, lambda value: value < 5, data))


def show_task_3_examples() -> None:
    print("\nTask 3 examples")
    passwords = PasswordGenerator(length=8, count=3)
    print(next(passwords))
    print(next(passwords))
    for password in passwords:
        print(password)


def show_task_4_and_5_examples() -> None:
    print("\nTask 4 examples")
    fib_gen = make_generator(fibonacci)
    print([next(fib_gen) for _ in range(6)])
    arithmetic_gen = make_generator(lambda n: 3 * n + 2)
    print([next(arithmetic_gen) for _ in range(5)])

    print("\nTask 5 examples")
    fib_mem_gen = make_generator_mem(fibonacci)
    print([next(fib_mem_gen) for _ in range(8)])


def show_task_6_examples() -> None:
    print("\nTask 6 examples")
    print(add(2, 3))
    demo = DemoClass("example")
    print(demo.label())


def main() -> None:
    configure_logging()
    show_task_1_examples()
    show_task_2_examples()
    show_task_3_examples()
    show_task_4_and_5_examples()
    show_task_6_examples()


if __name__ == "__main__":
    main()
