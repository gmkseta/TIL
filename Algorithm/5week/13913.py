import sys
from collections import deque

N, K = list(map(int, sys.stdin.readline().split()))

visited = [-1]*100_001
visited[N] = (0, None)
need_visited = deque()
need_visited.append(N)

move = [lambda x: x-1, lambda x: x + 1, lambda x: x*2]

counter = 0
result = []
while need_visited:
    point = need_visited.popleft()
    if point == K:
        result = visited[point]
        break
    for i in range(3):
        next_point = move[i](point)
        if 0 <= next_point <= 100_000 and visited[next_point] == -1:
            visited[next_point] = (visited[point][0]+1, point)
            need_visited.append(next_point)

print(result[0])
point = visited[point][1]
path = [K]
while True:
    if point is None:
        break
    path.append(point)
    point = visited[point][1]

path.reverse()
print(*path)
