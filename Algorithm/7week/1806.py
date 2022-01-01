import sys
input = sys.stdin.readline

N, S = list(map(int, input().split()))
numbers = list(map(int, input().split()))


start = 0
end = 1
result = N
sum = numbers[start]
if sum == S:
    result = 1
flag = 0

while not (start == end == N):
    if sum < S and end < N:
        sum += numbers[end]
        end += 1
    else:
        sum -= numbers[start]
        start += 1

    if sum >= S:
        result = min(result, end-start)
        flag = 1

if flag == 0:
    print(0)
else:
    print(result)