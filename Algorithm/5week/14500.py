import sys


N, M = list(map(int, sys.stdin.readline().split()))

board = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]


def calc(path):
    result = 0
    for point in path:
        result += board[point[0]][point[1]]
    return result


result = 0

max_val = max(map(max, board))

dpoint = [[1, 0], [0, 1], [-1, 0], [0, -1]]


visited = [([0] * M) for _ in range(N)]


def search(point, idx, total):
    global result
    if result >= total + max_val * (3-idx):
        return
    if idx == 3:
        result = max(result, total)
        return
    for i in range(4):
        dx, dy = dpoint[i]
        next_y, next_x = point[0]+dy, point[1]+dx
        if 0 <= next_y < N and 0 <= next_x < M and visited[next_y][next_x] == 0:
            if idx == 1:
                visited[next_y][next_x] = 1
                search(point, idx+1, total + board[next_y][next_x])
                visited[next_y][next_x] = 0

            visited[next_y][next_x] = 1
            search((next_y, next_x), idx+1, total + board[next_y][next_x])
            visited[next_y][next_x] = 0


for i in range(N):
    for j in range(M):
        visited[i][j] = 1
        search((i, j), 0, board[i][j])
        visited[i][j] = 0

print(result)
