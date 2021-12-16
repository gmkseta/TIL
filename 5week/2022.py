import sys
import math


def calc(x, y, w):
    h1 = math.sqrt(x**2-w**2)
    h2 = math.sqrt(y**2-w**2)
    c = h1*h2 / (h1+h2)
    return c


x, y, c = map(float, sys.stdin.readline().split())
left, right = 0, min(x, y)
mid = 0
while abs(right-left) > 1e-6:
    mid = (left+right)/2
    if calc(x, y, mid) >= c:
        left = mid
    else:
        right = mid
print("%.3f" % round(mid, 3))
