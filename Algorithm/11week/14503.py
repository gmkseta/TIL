import sys

input = sys.stdin.readline

N, M = list(map(int, input().split()))

r, c, d = list(map(int, input().split()))

board = [list(map(int, input().split())) for _ in range(N)]

direction = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0)
}


def solution(board, r, c, d):
    counter = 0
    while True:
        if board[r][c] == 0:
            counter += 1
        board[r][c] = 2
        for i in range(1, 6):
            if i == 5:
                dc, dr = direction[(d + 2) % 4]
                nr, nc = r + dr, c + dc

                if 0 <= nr < N and 0 <= nc < M and board[nr][nc] != 1:
                    r, c = nr, nc
                else:
                    return counter
            else:
                dc, dr = direction[(d + 3 * i) % 4]
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < M and board[nr][nc] == 0:
                    r, c, d = nr, nc, (d + 3 * i) % 4
                    break


print(solution(board, r, c, d))
