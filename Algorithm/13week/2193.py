import sys

input = sys.stdin.readline

n = int(input())

dp = [[0] * 2 for _ in range(n)]

dp[0][1] = 1

for i in range(1, n):
    dp[i][0] = dp[i - 1][1] + dp[i - 1][0]
    dp[i][1] = dp[i - 1][0]

print(sum(dp[n - 1]))
