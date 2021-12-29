import sys
import math
from collections import deque
import random
input = sys.stdin.readline

n, d = list(map(int, input().split()))

sensors = deque()
for _ in range(n):
    x, y = list(map(int, input().split()))
    sensors.append((x,y))



def distance(a, b):
    return math.sqrt(
        (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    )

graph = {i: set() for i in range(n)}
for i in range(n):
    for j in range(i, n):
        if distance(sensors[i], sensors[j]) <= d:
            graph[i].add(j)
            graph[j].add(i)

ans = set()
for i in range(n):
    current_point = i
    result = graph[i]
    visited = {i}
    while result:
        remain = visited ^ result
        if len(remain) == 0:
            break
        current_point = random.sample(list(remain), 1)[0]
        visited.add(current_point)
        result = (graph[current_point]) & result

    if len(ans) < len(result):
        ans = result


print(len(ans))
result = list(map(lambda x: x+1, ans))
result.sort()
print(*result)





