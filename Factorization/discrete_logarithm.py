from math import ceil, sqrt

from helpers import get_str_deg, get_str_idx
from factorization import trial_division
from gcd import xegcd
from chinese_theorem import crt


def baby_step_giant_step(a, b, p, *, show_solution=False):
    m = int(ceil(sqrt(p)))
    am = pow(a, m, p)

    giant_steps = {}
    temp = 1
    for i in range(1, m):
        temp = (temp * am) % p
        if temp not in giant_steps:
            giant_steps[temp] = i
            
    baby_steps = {}
    temp = b
    for j in range(m):
        if temp in giant_steps:
            baby_steps[temp] = j
            x = giant_steps[temp]*m - j
            break
        else:
            baby_steps[temp] = j
            temp = (temp * a) % p
    else:
        raise ValueError(f'{a} is not a generator of cyclic group Z{get_str_idx(p - 1)}')

    if show_solution:
        print(f'Solve: {a}ˣ = {b} mod({p})')
        print(f'm = ⌈√{p}⌉ = {m}')

        str_m_deg = get_str_deg(m)
        print('Giant steps:')
        for value, i in giant_steps.items():
            print(f'{a}⁽{get_str_deg(i)}*{str_m_deg}⁾ (mod {p}) = {value}')

        print('Baby steps:')
        for value, j in baby_steps.items():
            print(f'{b} × {a}{get_str_deg(j)} (mod {p}) = {value}')

        print(f'Answer: x = {giant_steps[temp]}×{m} − {baby_steps[temp]} = {x}\n')

    return x


def _dlog(a, b, p, show_solution=False):
    if a == b:
        x = 1
    elif b == 1:
        x = 0
    else:
        return baby_step_giant_step(a, b, p, show_solution=show_solution)

    if show_solution:
        print(f'Solve: {a}ˣ = {b} (mod {p})')
        print(f'Answer: x = {x}\n')

    return x


def pohlig_hellman(a, b, p, *, show_solution=False):
    order = p - 1
    factors = trial_division(order)
    a_inv = xegcd(a, p)[0]

    if show_solution:
        print(f'Solve: {a}ˣ = {b} (mod {p})')
        str_factors = '×'.join(f'{q}{get_str_deg(alpha)}' for q, alpha in factors)
        print(f'φ({p}) = {p} − 1 = {order} = {str_factors}')
        print(f'{a}⁻¹ (mod {p}) = {a_inv}\n')

    chinese_system = []
    for i, (q, alpha) in enumerate(factors, start=1):
        q_i = pow(q, alpha)
        a_xj_deg = int(order / q)
        a_xj = pow(a, a_xj_deg, p)
        b_xj_deg = a_xj_deg
        b_xj = pow(b, b_xj_deg, p)

        if show_solution:
            print(f'q{get_str_idx(i)} = {q}')
            str_x = 'x₀' + ''.join(f' + x{get_str_idx(i)}{q}{get_str_deg(i)}' for i in range(1, alpha))
            print(f'x = {str_x} (mod {q}{get_str_deg(alpha)})\n')
            print(f'Find x₀: '
                  f'{a}{get_str_deg(a_xj_deg)}ˣ = '
                  f'{b}{get_str_deg(b_xj_deg)} (mod {p}) '
                  f'where power of a={a} and b={b} is\n'
                  f'{a_xj_deg} = {order} / {q}')

        x = {0: _dlog(a_xj, b_xj, p, show_solution=show_solution)}
        ba_xj = b
        for j in range(1, alpha):
            a_inv_xj_deg = (x[j - 1] * pow(q, j - 1)) % q_i
            a_inv_xj = 1 if not a_inv_xj_deg else pow(a_inv, a_inv_xj_deg, p)
            b_xj_deg = int(b_xj_deg / q)
            ba_xj = (ba_xj * a_inv_xj) % p
            b_xj = pow(ba_xj, b_xj_deg, p)

            if show_solution:
                str_a_inv_xj_deg = sum(x.get(i) * pow(q, i) for i in range(j)) % q_i
                print(f'Find x{get_str_idx(j)}: '
                      f'{a}{get_str_deg(a_xj_deg)}ˣ = '
                      f'({b}×{a}⁻{get_str_deg(str_a_inv_xj_deg)}){get_str_deg(b_xj_deg)} (mod {p}) '
                      f'where powers of a={a} and b×a⁻{get_str_deg(str_a_inv_xj_deg)}={ba_xj} are\n'
                      f'{a_xj_deg} = {order} / {q}\n'
                      f'{b_xj_deg} = {order} / {q}{get_str_deg(j + 1)}\n'
                      f'{a_inv_xj_deg} = ∑xⱼ₋₁{q}ʲ⁻¹ where j = {j}')

            x[j] = _dlog(a_xj, b_xj, p, show_solution=show_solution)
        chinese_system.append((sum(x_i * pow(q, i) for i, x_i in x.items()) % q_i, q_i))

    x = crt(chinese_system, show_solution=show_solution)
    return x


if __name__ == '__main__':
    assert pow(2, baby_step_giant_step(2, 49, 101), 101) == 49
    assert pow(2, baby_step_giant_step(2, 49, 107), 107) == 49
    assert pow(3, baby_step_giant_step(3, 8576, 53047), 53047) == 8576
    pohlig_hellman(3, 77, 233, show_solution=True)
