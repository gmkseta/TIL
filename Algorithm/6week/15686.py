from itertools import combinations
import sys
input = sys.stdin.readline


N, M = list(map(int, input().split()))

chickens = []
homes = []

for i in range(N):
    row = list(map(int, input().split()))
    for j in range(N):
        if row[j] == 1:
            homes.append((i, j))
        elif row[j] == 2:
            chickens.append((i, j))


def chicken_distance(homes, chickens):
    distances = [float("inf")] * len(homes)

    for (c_y, c_x) in chickens:
        for idx, (h_y, h_x) in enumerate(homes):
            distances[idx] = min(abs(c_y-h_y) + abs(c_x - h_x), distances[idx])
    return sum(distances)


result = float('inf')
for remain_chickens in combinations(chickens, M):
    result = min(result, chicken_distance(homes, remain_chickens))

print(result)
