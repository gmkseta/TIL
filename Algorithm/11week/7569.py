from collections import deque

M, N, H = map(int, input().split())

board = []
need_to_visit = deque()
for h in range(H):
    floor = []
    for i in range(N):
        row = list(map(int, input().split()))
        floor.append(row)
        for j in range(M):
            if row[j] == 1:
                need_to_visit.append((i, j, h))
    board.append(floor)

DIRS = [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]

while need_to_visit:
    x, y, h = need_to_visit.popleft()
    for dx, dy, dh in DIRS:
        nx, ny, nh = x + dx, y + dy, h + dh
        if 0 <= nx < N and 0 <= ny < M and 0 <= nh < H:
            if board[nh][nx][ny] == 0:
                board[nh][nx][ny] = board[h][x][y] + 1
                need_to_visit.append((nx, ny, nh))

all_visited = True
for floor in board:
    for row in floor:
        for cell in row:
            if cell == 0:
                all_visited = False
if not all_visited:
    print(-1)
else:
    ans = 0
    for floor in board:
        for row in floor:
            for cell in row:
                ans = max(ans, cell)
    print(ans - 1)
