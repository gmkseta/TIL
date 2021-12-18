import sys
import heapq


N = int(sys.stdin.readline())

numbers = []
for _ in range(N):
    number = int(sys.stdin.readline())
    if number == 0:
        if numbers:
            print(heapq.heappop(numbers))
        else:
            print(0)
    else:
        heapq.heappush(numbers, number)
