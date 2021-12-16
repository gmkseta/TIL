import sys
import heapq
from collections import defaultdict


test_case = int(sys.stdin.readline())


for _ in range(test_case):
    n = int(sys.stdin.readline())
    min_arr = []
    max_arr = []
    num_counter = defaultdict(int)
    for i in range(n):
        O, N = sys.stdin.readline().rstrip().split()
        N = int(N)
        if O == 'I':
            num_counter[N] += 1
            heapq.heappush(min_arr, N)
            heapq.heappush(max_arr, -N)
        elif O == 'D' and len(min_arr) > 0:
            if N == 1:
                while max_arr:
                    key = -heapq.heappop(max_arr)
                    if num_counter.get(key):
                        num_counter[key] -= 1
                        break
            else:
                while min_arr:
                    key = heapq.heappop(min_arr)
                    if num_counter.get(key):
                        num_counter[key] -= 1
                        break

    result = [k for k, v in num_counter.items() if v > 0]

    if result:
        result.sort()
        print(result[-1], result[0])
    else:
        print("EMPTY")
