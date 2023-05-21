def generate(count, init=0):
    x = init
    while count > 0:
        count -= 1
        x = (13 * x ** 2 - 3 * x + 27 - 17 * x) % 65536
        yield x
