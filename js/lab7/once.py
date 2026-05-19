def once(fun):
    called = False

    def inner(*args, **kwargs):
        nonlocal called
        if called:
            return
        called = True
        return fun(*args, **kwargs)

    return inner


@once
def init():
    print("hello")


def main():
    init()
    init()
    init()


if __name__ == "__main__":
    main()
