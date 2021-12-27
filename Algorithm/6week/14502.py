from collections import deque
import sys
from itertools import combinations
input = sys.stdin.readline


N, M = list(map(int, input().split()))

board = []
virus = []
empty = []
wall_count = 0
for i in range(N):
    arr = list(map(int, input().split()))
    board.append(arr)
    for j in range(M):
        if arr[j] == 2:
            virus.append((i, j))
        elif arr[j] == 0:
            empty.append((i, j))

    wall_count += arr.count(1)

direction = [
    (1, 0),
    (-1, 0),
    (0, -1),
    (0, 1)
]


def infect(board):
    need_visit = deque()
    need_visit.extend(virus)

    visited = [0] * (N * M+1)

    while need_visit:
        y, x = need_visit.pop()
        if 0 <= y < N and 0 <= x < M and visited[y*M+x] == 0 and board[y][x] != 1:
            visited[y*M+x] = 1
            for i in range(4):
                dy, dx = direction[i]
                need_visit.append((dy+y, dx+x))

    return sum(visited)


result = 0
for new_walls in list(combinations(empty, 3)):
    new_board = [row[:] for row in board]
    for wall in new_walls:
        y, x = wall
        new_board[y][x] = 1
    result = max(result, (N*M - (infect(new_board)+wall_count+3)))

print(result)
