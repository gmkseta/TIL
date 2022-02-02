import sys

input = sys.stdin.readline

n = int(input())

glasses = [int(input()) for _ in range(n)]

dp = [[0] * 3 for _ in range(n)]

dp[0][1] = glasses[0]
dp[0][2] = glasses[0]

for i in range(1, n):
    dp[i][0] = max(dp[i - 1][1], dp[i - 1][2])
    dp[i][1] = max(dp[i - 1][0], dp[i - 2][0]) + glasses[i]
    dp[i][2] = dp[i - 1][1] + glasses[i]

print(max(dp[n - 1]))
