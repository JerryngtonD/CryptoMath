SUPERSCRIPTS = {digit: symbol
                for digit, symbol in enumerate(['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹'])}

SUBSCRIPTS = {digit: symbol
              for digit, symbol in enumerate(['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉'])}


def get_digits(number):
    digits = []
    while number:
        digits.append(number % 10)
        number //= 10
    return digits


def get_str_deg(degree):
    if degree in SUPERSCRIPTS:
        return SUPERSCRIPTS.get(degree)
    else:
        digits = get_digits(degree)
        return ''.join(SUPERSCRIPTS.get(digit) for digit in reversed(digits))


def get_str_idx(index):
    if index in SUBSCRIPTS:
        return SUBSCRIPTS.get(index)
    else:
        digits = get_digits(index)
        return ''.join(SUBSCRIPTS.get(digit) for digit in reversed(digits))
