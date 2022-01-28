import sys

input = sys.stdin.readline

T = int(input())


def in_cache(func):
    cache = {}

    def wrapper(n):
        if n in cache:
            return cache[n]
        else:
            cache[n] = func(n)
            return cache[n]

    return wrapper


@in_cache
def factorial_recursive(n):
    return n * factorial_recursive(n - 1) if n > 1 else 1


for _ in range(T):
    n, m = list(map(int, input().split()))
    print(int((factorial_recursive(m) // factorial_recursive(m - n)) // factorial_recursive(n)))
