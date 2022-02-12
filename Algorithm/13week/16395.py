import sys

input = sys.stdin.readline

n, k = list(map(int, input().split()))

dp = [[0] * (n + 1) for _ in range(n + 1)]

dp[0][0] = 1

for i in range(1, n):
    for j in range(0, i + 1):
        dp[i][j] = dp[i - 1][j] + dp[i - 1][j - 1]

print(dp[n - 1][k - 1])
