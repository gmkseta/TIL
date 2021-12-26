import sys
import bisect
import heapq


N = int(sys.stdin.readline())

assignments = {i: [] for i in range(1, 1001)}
for _ in range(N):
    day, score = list(map(int, sys.stdin.readline().split()))
    bisect.insort(assignments[day], score)

total_score = 0
for i in range(1000, 0, -1):
    if assignments[i]:
        score = assignments[i].pop()
        total_score += score
        if i != 1:
            assignments[i -
                        1] = list(heapq.merge(assignments[i], assignments[i-1]))

print(total_score)
