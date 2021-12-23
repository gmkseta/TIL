import sys
import heapq

n = int(sys.stdin.readline())


left_heap = []
right_heap = []
for size in range(1, n+1):
    k = int(sys.stdin.readline())
    if size == 1:
        left_heap.append((-k, k))
    elif size % 2 == 0:
        # 짝수일때 오른쪽 들어가는거면 그냥 넣고
        if k >= left_heap[0][1]:
            heapq.heappush(right_heap, k)
        else:
            # 아니면 heap left를 한번 옮겨준다.
            _, num = heapq.heappop(left_heap)
            heapq.heappush(right_heap, num)
            heapq.heappush(left_heap, (-k, k))
    elif size % 2 == 1:
        # 홀수일 때 왼쪽으로 들어가는거면 그냥 넣고
        if k <= left_heap[0][1]:
            heapq.heappush(left_heap, (-k, k))
        elif k > right_heap[0]:
            num = heapq.heappop(right_heap)
            heapq.heappush(left_heap, (-num, num))
            heapq.heappush(right_heap, k)
        else:
            heapq.heappush(left_heap, (-k, k))

    print(left_heap[0][1])
