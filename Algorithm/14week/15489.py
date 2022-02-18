import sys

input = sys.stdin.readline

r, c, w = list(map(int, input().split()))

n = r + w - 1

dp = [[0] * (n + 1) for _ in range(n + 1)]

dp[0][0] = 1

for i in range(1, n):
    for j in range(0, i + 1):
        dp[i][j] = dp[i - 1][j] + dp[i - 1][j - 1]

ans = 0

for i in range(r - 1, n):
    for j in range(c - 1, i + 1 - r + c):
        ans += dp[i][j]
print(ans)
