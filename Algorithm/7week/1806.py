import sys

input = sys.stdin.readline

N, S = list(map(int, input().split()))
numbers = list(map(int, input().split()))

start = 0
end = 1
result = N
s = numbers[start]
flag = 0

if s >= S:
    result = 1
    flag = 1
else:
    while not (start == end == N):
        if s < S and end < N:
            s += numbers[end]
            end += 1
        else:
            s -= numbers[start]
            start += 1

        if s >= S:
            result = min(result, end - start)
            flag = 1

if flag == 0:
    print(0)
else:
    print(result)
