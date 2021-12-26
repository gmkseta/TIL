import sys
from collections import deque


N, K = list(map(int, sys.stdin.readline().split()))
result = deque([])
for i in range(1, N + 1):
    result.append(i)
print('<', end='')
while result:
    for i in range(K - 1):
        result.append(result[0])
        result.popleft()
    print(result.popleft(), end='')
    if result:
        print(', ', end='')
print('>')
