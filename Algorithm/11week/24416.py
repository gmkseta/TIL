import sys

input = sys.stdin.readline

n = int(input())

dp = [1] * n
idx = 2

while idx < n:
    dp[idx] = dp[idx - 1] + dp[idx - 2]
    idx += 1

print(dp[-1], n - 2)
