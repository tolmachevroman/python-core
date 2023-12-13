from pprint import pprint as pp

scientists = [
    {'name': 'Ada Lovelace', 'field': 'math', 'born': 1815, 'nobel': False},
    {'name': 'Emmy Noether', 'field': 'math', 'born': 1882, 'nobel': False},
    {'name': 'Marie Curie', 'field': 'physics', 'born': 1867, 'nobel': True},
    {'name': 'Tu Youyou', 'field': 'chemistry', 'born': 1930, 'nobel': True},
    {'name': 'Ada Yonath', 'field': 'chemistry', 'born': 1939, 'nobel': True},
    {'name': 'Vera Rubin', 'field': 'astronomy', 'born': 1928, 'nobel': False},
    {'name': 'Sally Ride', 'field': 'physics', 'born': 1951, 'nobel': False}
]


if __name__ == "__main__":
    s = sorted(scientists, key=lambda x: x['name'])
    pp(s)

    def last_name(x): return x['name'].split()[-1]
    tesla = {'name': 'Nikola Tesla', 'field': 'physics',
             'born': 1856, 'nobel': False}
    print(last_name(tesla))
