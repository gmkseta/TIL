import sys
input = sys.stdin.readline

n = int(input())

solutions = list(map(int, input().split()))

result = float('inf')

ans_min = min_idx = 0
ans_max = max_idx = n-1
while max_idx > min_idx:
    part = solutions[min_idx] + solutions[max_idx]
    if abs(part) < result:
        result = abs(part)
        ans_min = min_idx
        ans_max = max_idx
    if part == 0:
        break
    elif part > 0:
        max_idx -= 1
    else:
        min_idx += 1

print(solutions[ans_min], solutions[ans_max])