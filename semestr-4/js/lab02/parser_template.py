from utils import base_parser


def main():
    @base_parser()
    def test(**_):
        return True

    _ = test


if __name__ == "__main__":
    main()
