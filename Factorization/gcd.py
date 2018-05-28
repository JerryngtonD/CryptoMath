from prettytable import PrettyTable


def xegcd(a, b, *, show_solution=False):
    """Extended Euclidean algorithm: d == ax + by

    :param a: 1st number
    :param b: 2nd number
    :param show_solution: print steps of algorithm if true
    :return: (x, y, d), where x and y -- Bezout coefficients, d -- greatest common divisor of a and b
    """
    if a < b:
        a, b = b, a
        swapped = True
    else:
        swapped = False
    
    x = [1, 0, a]
    y = [0, 1, b]
    steps = [x[:]]
    while y[2]:
        q, r = divmod(x[2], y[2])
        x[2], y[2] = y[2], r
        x[0], x[1] = x[1], x[0] - x[1]*q
        y[0], y[1] = y[1], y[0] - y[1]*q
        steps.append([x[0], y[0], x[2]])
    x, y, d = x[0], y[0], x[2]

    if show_solution:
        print(f'Solve: gcd({a}, {b})')
        
        table = PrettyTable(['x', 'y', 'd'])
        for step in steps:
            table.add_row(step)
        print(table)

        print(f'Answer: GCD of {a} and {b} is {d} == {a}×({x}) + {b}×({y})\n')
        
    return (x, y, d) if not swapped else (y, x, d)


if __name__ == '__main__':
    a = int(input('a = '))
    b = int(input('b = '))
    print(xegcd(a, b, show_solution=True))
