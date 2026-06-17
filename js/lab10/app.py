import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab10.web import main  # pylint: disable=wrong-import-position


if __name__ == "__main__":
    main()
