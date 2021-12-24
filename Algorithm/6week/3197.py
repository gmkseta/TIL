# import sys
# from collections import deque
# import time


# R, C = list(map(int, sys.stdin.readline().split()))

# swans = []
# board = []
# will_melted = set()
# directions = [
#     (-1, 0),
#     (0, 1),
#     (0, -1),
#     (1, 0)
# ]


# for i in range(R):
#     arr = list(sys.stdin.readline().rstrip())
#     # if i == 0:
#     #     arr = list(fir)
#     # elif i == R-1:
#     #     arr = list(last)
#     # else:
#     #     arr = list(comm)
#     board.append(arr)
#     if 'L' in arr:
#         x = arr.index('L')
#         swans.append((i, x))
#         board[i][x] = '.'
#         if len(swans) == 1 and arr.count('L') == 2:
#             x = arr.index('L', x+1)
#             swans.append((i, x))
#             board[i][x] = '.'
#     for j in range(C):
#         if arr[j] == '.':
#             for k in range(3):
#                 dy, dx = directions[k]
#                 ny, nx = i+dy, j+dx
#                 if 0 <= ny < R and 0 <= nx < C and board[ny][nx] == 'X':
#                     will_melted.add((ny, nx))
# print(will_melted)


# start, end = swans


# visited = [[-1]*C for _ in range(R)]


# before_melted = set()
# before_melted.add(start)


# def melt():
#     global will_melted
#     next_melted = set()
#     for (y, x) in will_melted:
#         board[y][x] = '.'
#         for i in range(4):
#             dy, dx = directions[i]
#             next_y = y+dy
#             next_x = x+dx
#             if 0 <= next_y < R and 0 <= next_x < C and board[next_y][next_x] == 'X':
#                 next_melted.add((next_y, next_x))
#     will_melted = next_melted


# def is_with_melt_adjacent():

#     global before_melted
#     need_visited = set(before_melted)
#     before_melted = set()
#     while need_visited:
#         y, x = need_visited.pop()
#         for i in range(4):
#             dy, dx = directions[i]
#             next_y = y+dy
#             next_x = x+dx
#             if (next_y, next_x) == end:
#                 return True
#             if 0 <= next_y < R and 0 <= next_x < C and visited[next_y][next_x] == -1:
#                 if board[next_y][next_x] == '.':
#                     need_visited.add((next_y, next_x))
#                     visited[next_y][next_x] = 0
#                 elif board[next_y][next_x] == 'X':
#                     before_melted.add((next_y, next_x))
#     return False


# counter = 0

# while not is_with_melt_adjacent():
#     counter += 1
#     melt()

# print(counter)

from collections import deque
import sys

input = sys.stdin.readline
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]


def bfs():
    while q:
        x, y = q.popleft()
        if x == x2 and y == y2:
            return 1
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < m and 0 <= ny < n:
                if not c[nx][ny]:
                    if a[nx][ny] == '.':
                        q.append([nx, ny])
                    else:
                        q_temp.append([nx, ny])
                    c[nx][ny] = 1
    return 0


def melt():
    while wq:
        x, y = wq.popleft()
        if a[x][y] == 'X':
            a[x][y] = '.'
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < m and 0 <= ny < n:
                if not wc[nx][ny]:
                    if a[nx][ny] == 'X':
                        wq_temp.append([nx, ny])
                    else:
                        wq.append([nx, ny])
                    wc[nx][ny] = 1


m, n = map(int, input().split())
c = [[0]*n for _ in range(m)]
wc = [[0]*n for _ in range(m)]

a, swan = [], []
q, q_temp, wq, wq_temp = deque(), deque(), deque(), deque()

for i in range(m):
    row = list(input().strip())
    a.append(row)
    for j, k in enumerate(row):
        if a[i][j] == 'L':
            swan.extend([i, j])
            wq.append([i, j])
        elif a[i][j] == '.':
            wc[i][j] = 1
            wq.append([i, j])

x1, y1, x2, y2 = swan
q.append([x1, y1])
a[x1][y1], a[x2][y2], c[x1][y1] = '.', '.', 1
cnt = 0

while True:
    melt()
    if bfs():
        print(cnt)
        break
    q, wq = q_temp, wq_temp
    q_temp, wq_temp = deque(), deque()
    cnt += 1
