import sys

input = sys.stdin.readline

N, M = list(map(int, input().split()))
memories = list(map(int, input().split()))
costs = list(map(int, input().split()))
_sum = sum(costs)

dp = [0] * (_sum + 1)

for i in range(1, N + 1):

    for j in range(_sum, -1, -1):

        if j - costs[i - 1] >= 0:
            dp[j] = max(dp[j], dp[j - costs[i - 1]] + memories[i - 1])

for i in range(_sum + 1):
    if dp[i] >= M:
        print(i)
        break
