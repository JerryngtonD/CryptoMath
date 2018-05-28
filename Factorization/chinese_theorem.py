from functools import reduce
from operator import mul

from gcd import xegcd
from helpers import get_str_idx


def crt(chinese_system, *, show_solution=False):
    rems, mods = zip(*chinese_system)
    M = reduce(mul, mods)
    m = [int(M / mod) for mod in mods]
    x = []
    m_inverses = []
    for a_i, m_i, r_i in zip(mods, m, rems):
        m_inverse_i = xegcd(m_i, a_i)[0]
        x.append((r_i * m_i * m_inverse_i) % M)
        m_inverses.append(m_inverse_i)
    x = int(sum(x_i for x_i in x) % M)

    if show_solution:
        print('Solve system:')
        print('┌')
        for r_i, a_i in zip(rems, mods):
            print(f'│ x = {r_i} (mod {a_i})')
        print('└')

        print(f'M = {M}')
        for i, (a_i, m_i, m_inverse_i) in enumerate(zip(mods, m, m_inverses)):
            str_m_idx = get_str_idx(i)
            print(f'M{str_m_idx} = {m_i}, M{str_m_idx}⁽⁻¹⁾ = {m_inverse_i} (mod {a_i})')

        str_x_sum = ' + '.join(f'{r_i}×{m_i}×{m_inverse_i}' for r_i, m_i, m_inverse_i in zip(rems, m, m_inverses))
        print(f'Answer: x = {str_x_sum} = {x}')

    return x
