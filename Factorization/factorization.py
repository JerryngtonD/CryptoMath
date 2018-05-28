from collections import Counter
from math import ceil, sqrt

PERFECT_SQUARES_MOD_10 = [(0, 4, 6), (1, 5, 9)]


def trial_division(n):
    factors = []
    d = 2
    while n > 1:
        while not n % d:
            factors.append(d)
            n /= d
        d += 1
        if d * d > n:
            if n > 1:
                factors.append(int(n))
            break
    return [factor for factor in Counter(factors).items()]


def fermat_factor(n, *, show_solution=False):
    factors = []

    while not n % 2:
        factors.append((2, 1))
        n //= 2

    if n > 1:
        n_mod_10 = n % 10
        a_is_odd = 1 if n % 4 == 1 else 0
        a2_mod_10 = []

        if show_solution:
            print(f'Solve: factorize {n} using Fermat\'s Method: N = a² − b² = {n}\n')
            print(f'0, 1, 4, 5, 6 and 9 are perfect squares modulo 10\n')
            odd_or_even, equal_or_not = (('odd', 'even'), '=') if a_is_odd else (('even', 'odd'), '≠')
            print(f'a is {odd_or_even[0]} and b is {odd_or_even[1]}, because {n} {equal_or_not} 1 (mod 4)\n')
            print(f'Because N is {n}, then N = {n_mod_10} (mod 10) so possible values of a² are:')

        for b2 in PERFECT_SQUARES_MOD_10[not a_is_odd]:
            a2 = (n_mod_10+b2) % 10
            if a2 in PERFECT_SQUARES_MOD_10[a_is_odd]:
                a2_mod_10.append(a2)

            if show_solution:
                print(f'a² = {n_mod_10} + {b2} = {a2} (mod 10)')

        a_mod_10 = [a
                    for a in range(10)
                    for a2 in a2_mod_10
                    if pow(a, 2, 10) == a2]

        if show_solution:
            if len(a2_mod_10) > 1:
                str_a2_mod_10 = ', '.join(str(i) for i in a2_mod_10[:-1]) + ' or ' + str(a2_mod_10[-1])
            else:
                str_a2_mod_10 = str(a2_mod_10[0])
            print(f"\nSo a² is {str_a2_mod_10} is a perfect square "
                  f"and an {('even', 'odd')[a_is_odd]} number (modulo 10)")
            print(f"So a ends in the digit {', '.join(str(i) for i in a_mod_10[:-1])} or {a_mod_10[-1]}:")

        for a in range(ceil(sqrt(n)), ((n+1)//2) + 1):
            if a % 10 in a_mod_10:
                b2 = a*a - n
                b = sqrt(b2)
                if not ceil(b % 1):
                    b = int(b)
                    c = int(a + b)
                    d = int(a - b)

                    if show_solution:
                        print(f'{a}² − {n} = {b}² (a perfect square)')
                        print(f'\nAnswer: N = ({a} + {b})({a} − {b}) = {c} × {d}')

                    if c == n and d == 1:
                        factors.append((c, 1))
                        break
                    else:
                        factors.extend(fermat_factor(c))
                        factors.extend(fermat_factor(d))
                        break

                if show_solution:
                    print(f'{a}² − {n} = {b2} (not a perfect square)')

        else:
            factors.append((n, 1))

    factors_dict = {}
    for factor, deg in factors:
        factors_dict[factor] = factors_dict.setdefault(factor, 0) + deg
    return [factor for factor in factors_dict.items()]


if __name__ == '__main__':
    #assert fermat_factor(507473) == [(997, 1), (509, 1)]
    #assert fermat_factor(11093351, show_solution=True) == [(3803, 1), (2917, 1)]
    #assert fermat_factor(12335083) == [(4001, 1), (3083, 1)]
    fermat_factor(9240677, show_solution=True)
