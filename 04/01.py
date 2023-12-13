from resolver import Resolver


if __name__ == "__main__":
    resolve = Resolver()
    print(resolve("google.com"))
    print(resolve._cache)
    print(resolve.has_host("google.com"))
    resolve.clear()
    print(resolve._cache)
    print(resolve.has_host("google.com"))
