from collections import deque

T = int(input())
get_distance = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])


def bfs(start, end, points):
    q = deque([start])
    visited = [False] * (end + 2)
    visited[start] = True
    while q:
        cur = q.popleft()
        if cur == end:
            return "happy"
        for i in range(end + 1):
            if not visited[i] and get_distance(points[cur], points[i]) <= 50 * 20:
                q.append(i)
                visited[i] = True
    return "sad"


for _ in range(T):
    n = int(input())
    points = [list(map(int, input().split())) for _ in range(n + 2)]
    print(bfs(0, n + 1, points))
