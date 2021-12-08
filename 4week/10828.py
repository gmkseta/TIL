import sys
from collections import deque


n = int(sys.stdin.readline())


queue = deque()

for _ in range(n):
    command = sys.stdin.readline().rstrip().split()
    if command[0] == 'push':
        queue.append(command[1])
    elif command[0] == 'top':
        if len(queue) == 0:
            print('-1')
        else:
            print(queue[-1])
    elif command[0] == 'empty':
        print(
            0 if len(queue) else 1
        )
    elif command[0] == 'size':
        print(len(queue))
    elif command[0] == 'pop':
        if len(queue) == 0:
            print(-1)
        else:
            print(queue.pop())
