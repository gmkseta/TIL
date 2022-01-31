import sys
from collections import deque

input = sys.stdin.readline

N, M = list(map(int, input().split()))
direction = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Ice:

    def __init__(self):
        self.ices = set()
        self.board = []

        for i in range(N):
            self.board.append(list(map(int, input().split())))
            for j in range(M):
                if self.board[i][j] != 0:
                    self.ices.add((i, j))

    def solution(self):
        if N * M == len(self.ices):
            return 0
        self.melt()
        count = 1
        while len(self.ices) > 0 and self.check():
            self.melt()
            count += 1
        if len(self.ices) == 0:
            return 0
        else:
            return count

    def check(self):
        start = self.ices.pop()
        self.ices.add(start)
        need_visited = deque([start])
        visited = set([start])
        while need_visited:
            x, y = need_visited.popleft()
            for i in range(4):
                nx, ny = x + direction[i][0], y + direction[i][1]
                if N > nx >= 0 <= ny < M and (nx, ny) not in visited and 0 != self.board[nx][ny]:
                    need_visited.append((nx, ny))
                    visited.add((nx, ny))
        return len(self.ices) == len(visited)

    def melt(self):
        new_ices = set()
        new_high = {}
        for (x, y) in self.ices:
            high = self.board[x][y]
            for dx, dy in direction:
                nx, ny = x + dx, y + dy
                if N > nx >= 0 <= ny < M and self.board[nx][ny] == 0:
                    high -= 1
                if high == 0:
                    break
            if high != 0:
                new_ices.add((x, y))
                new_high[(x, y)] = high

        for (x, y) in self.ices:
            if (x, y) not in new_high:
                self.board[x][y] = 0
            else:
                self.board[x][y] = new_high[(x, y)]
        self.ices = new_ices


print(Ice().solution())
