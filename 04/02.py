def sequence_class(immutable):
    return tuple if immutable else list


if __name__ == "__main__":
    seq = sequence_class(immutable=True)
    t = seq("Timbuktu")
    print(t)
    print(type(t))
    seq = sequence_class(immutable=False)
    l = seq("Nairobi")
    print(l)
    print(type(l))
