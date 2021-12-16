import sys
from collections import deque

N, K = list(map(int, sys.stdin.readline().split()))
MAX = 100_000


def move(x, counter):
    result = []
    if x - 1 >= 0:
        result.append((x-1, counter+1))
    if x + 1 <= MAX:
        result.append((x+1, counter+1))
    return result


used = [0]*(MAX+1)


def teleport(x, counter):
    result = []
    while 0 < x <= MAX:
        if used[x] == 0:
            result.append((x, counter))
        x *= 2
    return result


need_visit = deque()
need_visit.append((N, 0))


while need_visit:
    point, counter = need_visit.popleft()
    if used[point] == 0:
        if point == K:
            print(counter)
            break
        used[point] = 1
        need_visit.extendleft(teleport(point, counter))
        need_visit.extend(move(point, counter))
