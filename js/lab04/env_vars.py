import os
import sys
from typing import Optional


def get_env_vars(filters: Optional[list[str]] = None) -> dict[str, str]:
    env_vars = dict(os.environ)
    if filters:
        filters_lower = [f.lower() for f in filters]
        env_vars = {
            k: v
            for k, v in env_vars.items()
            if any(f in k.lower() for f in filters_lower)
        }
    return env_vars


def print_env_vars(env_vars: dict[str, str]) -> None:
    for key in sorted(env_vars.keys()):
        print(f"{key}={env_vars[key]}")


def main() -> None:
    filters: Optional[list[str]] = sys.argv[1:] if len(sys.argv) > 1 else None
    env_vars = get_env_vars(filters)
    print_env_vars(env_vars)


if __name__ == "__main__":
    main()
