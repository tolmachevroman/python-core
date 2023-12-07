from math import factorial
from pprint import pprint as pp
import itertools


def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(x ** 0.5)+1):
        if x % i == 0:
            return False
    return True


def gen123():
    yield 1
    yield 2
    yield 3


if __name__ == '__main__':
    # List comprehensions
    words = "Why sometimes I have believed as many as six impossible things before breakfast".split()
    print(words)
    print([len(word) for word in words])
    print([str(factorial(x)) for x in range(20)])

    # Dict comprehensions
    country_to_capital = {'United Kingdom': 'London',
                          'Brazil': 'Brazilia',
                          'Morocco': 'Rabat',
                          'Sweden': 'Stockholm'}
    capital_to_country = {capital: country for country,
                          capital in country_to_capital.items()}
    pp(capital_to_country)

    # Filter comprehensions
    primes = [x for x in range(101) if is_prime(x)]
    print(primes)

    # Set comprehensions

    # Iteration protocols
    iterable = ['Spring', 'Summer', 'Autumn', 'Winter']
    iterator = iter(iterable)
    print(next(iterator))
    print(next(iterator))

    # Generators
    for i in gen123():
        print(i)

    million_squares = (x*x for x in range(1, 1000001))
    first_ten = itertools.islice(million_squares, 10)
    print(list(x for x in first_ten))
