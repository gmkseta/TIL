import sys


N, M = list(map(int, sys.stdin.readline().split()))

graph = {i: [] for i in range(1, N+1)}

bacons = []

for _ in range(M):
    _from, _to = list(map(int, sys.stdin.readline().split()))
    graph[_from].append(_to)
    graph[_to].append(_from)


for i in range(1, N+1):
    need_visited = [(i, 0)]
    visited = [float('inf')]*N
    while need_visited:
        point, dist = need_visited.pop()
        visited[point-1] = dist
        for p in graph[point]:
            if visited[p-1] > dist+1:
                need_visited.append((p, dist+1))

    bacons.append(sum(visited))

print(bacons.index(min(bacons))+1)
