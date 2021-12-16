import sys


N, M = list(map(int, sys.stdin.readline().split()))

woods = list(map(int, sys.stdin.readline().split()))

up = max(woods)
down = 0
mid = (up+down)//2


before_val = float('inf')


def cut(h):
    return sum(wood-h for wood in woods if wood-h > 0)


while True:
    val = cut(mid)
    if val >= M:
        down = mid
        mid = (up+down)//2
    elif val < M:
        up = mid
        mid = (up + down)//2
    if up - down <= 1:
        mid = down
        break

print(mid)
