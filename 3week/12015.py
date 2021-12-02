# import sys


# n = int(sys.stdin.readline())


# numbers = list(map(int, sys.stdin.readline().split()))

# dp = [0]*n

# for i in range(n):
#     for j in range(i):
#         if numbers[j] < numbers[i]:
#             dp[i] = max(dp[j]+1, dp[i])

# print(max(dp)+1)

import bisect
import sys


n = int(sys.stdin.readline())

numbers = list(map(int, sys.stdin.readline().split()))

stack = [0]

for i in numbers:
    if stack[-1] < i:
        stack.append(i)
    else:
        stack[bisect.bisect_left(stack, i)] = i

print(len(stack)-1)
