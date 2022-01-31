from collections import deque

n = int(input())

board = []
max_high = -float("inf")
min_high = float("inf")

for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        max_high = max(max_high, row[j])
        min_high = min(min_high, row[j])
    board.append(row)

direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def bfs(h):
    visited = [False] * n * n
    counter = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] - h > 0 and not visited[i * n + j]:
                counter += 1
                need_visited = deque([(i, j)])
                while need_visited:
                    x, y = need_visited.popleft()
                    for dx, dy in direction:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and not visited[nx * n + ny] and board[nx][ny] - h > 0:
                            need_visited.append((nx, ny))
                            visited[nx * n + ny] = True
    return counter


ans = 1
for h in range(min_high, max_high):
    ans = max(bfs(h), ans)
print(ans)
