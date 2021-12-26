import sys


N, M, B = list(map(int, sys.stdin.readline().split()))

min_h = float("inf")
max_h = 0
board = []
for _ in range(N):
    arr = list(map(int, sys.stdin.readline().split()))
    max_h = max(max(arr), max_h)
    min_h = min(min(arr), min_h)
    board.append(arr)


result = float('inf')
height = float('inf')
for h in range(max_h, min_h-1, -1):
    counter = 0
    current_blocks = B
    for i in range(N):
        for j in range(M):
            dh = h - board[i][j]
            if dh < 0:
                counter += -1*dh*2
                current_blocks -= dh
            elif dh > 0:
                counter += dh
                current_blocks -= dh
    if current_blocks < 0:
        pass
    elif counter < result:
        result = counter
        height = h

print(result, height)
