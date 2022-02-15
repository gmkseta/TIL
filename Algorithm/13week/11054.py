import bisect
import sys

n = int(sys.stdin.readline())

numbers = list(map(int, sys.stdin.readline().split()))

stack = [-1000000001]

ans = 0

for end in range(n + 1):
    stack = [0]

    temp_ans = 0
    for i in numbers[:end]:
        if stack[-1] < i:
            stack.append(i)
        else:
            stack[bisect.bisect_left(stack, i)] = i
    temp_ans += len(stack) - 1
    if end == n:
        stack = [-1001]
    else:
        stack = [-numbers[end - 1]]

    for num in numbers[end:]:

        if stack[-1] < -num:
            stack.append(-num)
        else:
            stack[bisect.bisect_left(stack, -num)] = -num

    temp_ans += len(stack) - 1

    ans = max(ans, temp_ans)

print(ans)
