import sys
from collections import deque


N, K = list(map(int, sys.stdin.readline().split()))

visited = [-1]*100_001
need_visited = deque()
need_visited.append((N, 0))


def move(point, time):
    return [(point + 1, time+1), (point - 1, time+1), (2 * point, time+1)]


while need_visited:
    point, time = need_visited.popleft()
    if point == K:
        print(time)
        break
    if 0 <= point <= 100_000 and visited[point] == -1:
        visited[point] = 1
        need_visited.extend(move(point, time))
