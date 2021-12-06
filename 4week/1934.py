import sys


def gcf(a, b):
    while b:
        a, b = b, a % b
    return a


n = int(sys.stdin.readline())
for _ in range(n):
    A, B = list(map(int, sys.stdin.readline().split()))
    print(A*B//gcf(A, B))
