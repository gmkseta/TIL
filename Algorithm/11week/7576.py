from collections import deque

M, N = map(int, input().split())

board = []
need_to_visit = deque()
for i in range(N):
    row = list(map(int, input().split()))
    board.append(row)
    for j in range(M):
        if row[j] == 1:
            need_to_visit.append((i, j))

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

while need_to_visit:
    x, y = need_to_visit.popleft()
    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < M and board[nx][ny] == 0:
            board[nx][ny] = board[x][y] + 1
            need_to_visit.append((nx, ny))

all_visited = True
for row in board:
    for col in row:
        if col == 0:
            all_visited = False
            break

if not all_visited:
    print(-1)
else:
    max_val = 0
    for row in board:
        for col in row:
            max_val = max(max_val, col)
    print(max_val - 1)
