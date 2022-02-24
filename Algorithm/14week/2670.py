import math

n = int(input())

arr = [float(input()) for _ in range(n)]

dp = arr[:]

for i in range(1, n):
    dp[i] = max(dp[i], dp[i - 1] * arr[i])

print("%.3f" % max(dp))
