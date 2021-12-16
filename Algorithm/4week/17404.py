import sys

n = int(sys.stdin.readline())

cost = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]


result = float('inf')
for initcolor in range(3):
    dp = [[float('inf')] * 3 for _ in range(n)]
    for i in range(3):
        if i == initcolor:
            dp[0][i] = cost[0][i]
            continue
        dp[0][i] = float('inf')

    for i in range(1, n):
        for j in range(3):
            dp[i][j] = cost[i][j] + min(dp[i-1][:j] + dp[i-1][j+1:])
    result = min(result, *(dp[-1][:initcolor] + dp[-1][initcolor+1:]))

print(result)
