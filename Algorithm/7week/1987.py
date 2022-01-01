import sys
from collections import deque
input = sys.stdin.readline

R, C = list(map(int, input().split()))

board = [list(input().rstrip()) for _ in range(R)]

direction = [(-1,0), (1,0), (0,-1), (0,1)]


def solution():
  result = 0
  need_visited = set()
  need_visited.add((0,0, board[0][0]))
  while need_visited:
    y, x, paths = need_visited.pop()
    result = max(result, len(paths))
    for dy,dx in direction:
      ny, nx = dy+y, dx+x
      if 0 <= ny < R and 0 <= nx < C and board[ny][nx] not in paths:
        need_visited.add((ny,nx, paths+board[ny][nx]))
      
  return result

print(solution())

