import sys
import heapq


n = int(sys.stdin.readline())

heap = []


for _ in range(n):
    numbers = list(map(int, sys.stdin.readline().split()))

    if not heap:
        for i in numbers:
            heapq.heappush(heap, i)
    else:
        for i in numbers:
            if heap[0] < i:
                heapq.heappush(heap, i)
                heapq.heappop(heap)

print(heap[0])
