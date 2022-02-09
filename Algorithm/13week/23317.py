n = int(input())
m = int(input())

case = {}
for i in range(m):
    row, col = map(int, input().split())
    case[row] = col

dp = [[0] * (n + 1) for _ in range(n + 1)]
dp[0][0] = 1

for i in range(1, n):
    for j in range(i + 1):
        dp[i][j] = dp[i - 1][j] + dp[i - 1][j - 1]

    if i in case:
        for j in range(i + 1):
            if j != case[i]:
                dp[i][j] = 0

print(sum(dp[n - 1]))
