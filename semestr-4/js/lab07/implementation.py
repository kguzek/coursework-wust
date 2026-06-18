from __future__ import annotations

import inspect
import logging
import random
import string
import time
from collections import defaultdict
from collections.abc import Callable, Generator, Iterable, Iterator, Sequence
from functools import lru_cache, wraps
from typing import Any, TypeVar


T = TypeVar("T")
R = TypeVar("R")


def acronym(words: Sequence[str]) -> str:
    return "".join(word[:1].upper() for word in words)


def median(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("median requires at least one value")
    sorted_values = sorted(values)
    mid = len(sorted_values) // 2
    return (
        sorted_values[mid]
        if len(sorted_values) % 2
        else (sorted_values[mid - 1] + sorted_values[mid]) / 2
    )


def sqrt_newton(x: float, epsilon: float = 1e-10) -> float:
    if x < 0:
        raise ValueError("x must be non-negative")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if x == 0:
        return 0.0

    def step(guess: float) -> float:
        return 0.5 * (guess + x / guess)

    def iterate(guess: float) -> float:
        next_guess = step(guess)
        return (
            next_guess
            if abs((next_guess * next_guess) - x) < epsilon
            else iterate(next_guess)
        )

    return iterate(x if x >= 1 else 1.0)


def make_alpha_dict(text: str) -> dict[str, list[str]]:
    words = text.split()
    keys = sorted({char for char in text if char.isalpha()})
    return {char: [word for word in words if char in word] for char in keys}


def flatten(items: list[Any] | tuple[Any, ...]) -> list[Any]:
    def reduce_item(item: Any) -> list[Any]:
        return flatten(item) if isinstance(item, (list, tuple)) else [item]

    return [value for item in items for value in reduce_item(item)]


def group_anagrams(words: Sequence[str]) -> dict[str, list[str]]:
    grouped: defaultdict[str, list[str]] = defaultdict(list)
    _ = [grouped["".join(sorted(word))].append(word) for word in words]
    return dict(grouped)


def forall(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return all(map(pred, iterable))


def exists(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return any(map(pred, iterable))


def atleast(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return sum(map(pred, iterable)) >= n


def atmost(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    if n <= 0:
        raise ValueError("n must be a positive integer")
    return sum(map(pred, iterable)) <= n


class PasswordGenerator(Iterator[str]):
    def __init__(
        self,
        length: int,
        charset: str = string.ascii_letters + string.digits,
        count: int = 1,
    ) -> None:
        if length <= 0:
            raise ValueError("length must be positive")
        if count < 0:
            raise ValueError("count must be non-negative")
        if not charset:
            raise ValueError("charset must not be empty")

        self.length = length
        self.charset = charset
        self.count = count
        self._generated = 0

    def __iter__(self) -> PasswordGenerator:
        return self

    def __next__(self) -> str:
        if self._generated >= self.count:
            raise StopIteration
        self._generated += 1
        return "".join(random.choice(self.charset) for _ in range(self.length))


def make_generator(f: Callable[[int], R]) -> Generator[R, None, None]:
    index = 1
    while True:
        yield f(index)
        index += 1


def make_generator_mem(f: Callable[[int], R]) -> Generator[R, None, None]:
    return make_generator(lru_cache(maxsize=None)(f))


def log(
    level: int = logging.INFO,
) -> Callable[[Callable[..., R] | type], Callable[..., R] | type]:
    logger = logging.getLogger(__name__)

    def decorator(target: Callable[..., R] | type) -> Callable[..., R] | type:
        if inspect.isclass(target):
            original_init = target.__init__

            @wraps(original_init)
            def wrapped_init(self: Any, *args: Any, **kwargs: Any) -> None:
                logger.log(
                    level,
                    "instantiating %s args=%s kwargs=%s",
                    target.__name__,
                    args,
                    kwargs,
                )
                original_init(self, *args, **kwargs)

            target.__init__ = wrapped_init
            return target

        @wraps(target)
        def wrapped(*args: Any, **kwargs: Any) -> R:
            started = time.perf_counter()
            logger.log(
                level,
                "call %s args=%s kwargs=%s",
                target.__name__,
                args,
                kwargs,
            )
            result = target(*args, **kwargs)
            duration = time.perf_counter() - started
            logger.log(
                level,
                "done %s result=%s duration=%.6fs",
                target.__name__,
                result,
                duration,
            )
            return result

        return wrapped

    return decorator


def fibonacci(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    if n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
