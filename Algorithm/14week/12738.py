import bisect
import sys

n = int(sys.stdin.readline())

numbers = list(map(int, sys.stdin.readline().split()))

stack = [-1000000001]

for i in numbers:
    if stack[-1] < i:
        stack.append(i)
    else:
        stack[bisect.bisect_left(stack, i)] = i

print(len(stack) - 1)
