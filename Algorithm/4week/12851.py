import sys
from collections import deque


N, K = list(map(int, sys.stdin.readline().split()))


need_visited = deque()
need_visited.append((N, 0))
visited = [False]*100_001


def next_point(point):
    x, n = point[0], point[1]
    n += 1
    result = []

    if x-1 >= 0 and not visited[x-1]:
        result.append((x-1, n))
    if x+1 <= 100_000 and not visited[x+1]:
        result.append((x+1, n))
    if 2*x <= 100_000 and not visited[2*x]:
        result.append((2*x, n))
    return result


while need_visited:
    point = need_visited.popleft()
    visited[point[0]] = True
    if point[0] == K:
        print(point[1])
        print(1+sum(p[0] == K and point[1] == p[1] for p in need_visited))
        break

    need_visited.extend(next_point(point))
