import sys

n = int(sys.stdin.readline())
points = []

for _ in range(n):
    M, N = list(map(int, sys.stdin.readline().split()))
    points.append((N, M))

points.sort()

for i in points:
    print(i[1], i[0])
