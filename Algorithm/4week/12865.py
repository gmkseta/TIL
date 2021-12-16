import sys

N, K = list(map(int, sys.stdin.readline().split()))


arr = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]

dp = [0]*(K+1)

for weight, val in arr:
    for j in range(K, weight - 1, -1):
        dp[j] = max(dp[j], dp[j-weight]+val)

print(dp[K])
