import sys
import heapq


test_case = int(sys.stdin.readline())


for _ in range(test_case):
    n = int(sys.stdin.readline())
    min_heap = []

    for i in range(n):
        O, N = sys.stdin.readline().rstrip().split()
        N = int(N)
        if O == 'I':
            heapq.heappush(min_heap, N)
        elif O == 'D' and len(min_heap) > 0:
            if N == 1:
                min_heap.pop()
            else:
                min_heap.pop(0)
    if len(min_heap) == 0:
        print("EMPTY")
    else:
        print(min_heap[-1], min_heap[0])
