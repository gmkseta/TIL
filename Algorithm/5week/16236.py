import sys
from collections import deque


N = int(sys.stdin.readline())

board = []
start = None
for i in range(N):
    board.append(list(map(int, sys.stdin.readline().split())))
    if 9 in board[i]:
        start = (i, board[i].index(9))


def move(point, size):
    y, x = point
    result = []
    if y-1 >= 0 and board[y-1][x] <= size:
        result.append((y-1, x))
    if x-1 >= 0 and board[y][x-1] <= size:
        result.append((y, x-1))
    if y+1 < N and board[y+1][x] <= size:
        result.append((y+1, x))
    if x+1 < N and board[y][x+1] <= size:
        result.append((y, x+1))
    return result


size = 2
counter = 0


def calculate_dist():
    need_visit = deque()
    need_visit.append([start])
    visited = [[0]*N for _ in range(N)]
    fish = []
    while need_visit:
        path = need_visit.popleft()
        point = path[-1]
        if 0 < board[point[0]][point[1]] < size:
            fish.append((len(path)-1, *point))
        for next_point in move(point, size):
            if visited[next_point[0]][next_point[1]] == 0:
                need_visit.append(path + [next_point])
                visited[next_point[0]][next_point[1]] = 1
    fish.sort()
    if fish:
        return fish[0]
    else:
        return [False, False, False]


result = 0
counter = 0
board[start[0]][start[1]] = 0

while True:
    dist, y, x = calculate_dist()
    if dist:
        board[y][x] = 0
        start = (y, x)
        result += dist
        counter += 1
        if counter == size:
            size += 1
            counter = 0
    else:
        break

print(result)
