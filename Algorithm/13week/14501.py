import sys

input = sys.stdin.readline

n = int(input())

arr = [list(map(int, input().split())) for _ in range(n)]

dp = [0] * 29

for i in range(n):
    cost, value = arr[i]
    dp[i + cost - 1] = max(dp[i + cost - 1], dp[i - 1] + value)
    dp[i] = max(dp[i], dp[i - 1])

print(dp[n - 1])
