import sys

input = sys.stdin.readline
N = int(input())
M = int(input())

distance = [[float('inf')] * N for _ in range(N)]

for i in range(N):
    distance[i][i] = 0
for _ in range(M):
    i, j, v = list(map(int, input().split()))
    distance[i - 1][j - 1] = min(distance[i - 1][j - 1], v)

# floyd_warshall
for k in range(N):
    for i in range(N):
        for j in range(N):
            if i == j or i == k or j == k:
                continue
            distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])

for i in range(N):
    for j in range(N):
        if distance[i][j] == float('inf'):
            distance[i][j] = 0

for i in distance:
    print(*i)
