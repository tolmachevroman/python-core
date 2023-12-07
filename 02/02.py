

import sys


def heron_sqrt(n):
    """Compute the square root of n using Heron's method."""
    if n < 0:
        raise ValueError(f'Cannot compute square root of negative number {n}')

    guess = n / 2  # Initial guess
    while True:
        new_guess = (guess + n / guess) / 2
        if abs(new_guess - guess) < 1e-6:  # Check for convergence
            return new_guess
        guess = new_guess


if __name__ == "__main__":
    try:
        print(heron_sqrt(10))
        print(heron_sqrt(-2))
        print(heron_sqrt(9))
    except ValueError as e:
        print(e, file=sys.stderr)
