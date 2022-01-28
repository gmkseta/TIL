import sys

input = sys.stdin.readline

A = list(map(int, list(input().rstrip())))
B = list(map(int, list(input().rstrip())))

dp = []
for (a, b) in zip(A, B):
    dp.append(a)
    dp.append(b)

for i in range(len(dp) - 1, 1, -1):
    for j in range(i):
        dp[j] = (dp[j + 1] + dp[j]) % 10

print("".join(map(str, dp[:2])))
