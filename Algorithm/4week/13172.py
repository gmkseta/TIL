import sys
import math


def exp(b, k):
    if k == 1:
        return b
    if k & 1:
        return b * exp(b, k-1) % MOD
    res = exp(b, k//2)
    return res*res % MOD


MOD = 1000000007
n = int(sys.stdin.readline())
for _ in range(n):
    N, S = list(map(int, sys.stdin.readline().split()))
    g = math.gcd(N, S)
    S //= g
    N //= g
    print(S * exp(N, MOD-2) % MOD)
