import sys
from collections import deque
input = sys.stdin.readline

n = int(input())

direction = [
    lambda x: x // 2 if x % 2 == 0 else 0,
    lambda x: x // 3 if x % 3 == 0 else 0,
    lambda x: x - 1
]


need_visited = deque()
need_visited.append(n)
visited = [(0,0)]*(n+1)

def sol():
    while need_visited:
        point = need_visited.popleft()
        for i in range(3):
            next_point = direction[i](point)
            if next_point and visited[next_point][0] == 0:
                need_visited.append(next_point)
                visited[next_point] = (visited[point][0] + 1, point)
                if next_point == 1:
                    return visited[next_point]
    return (0,1)
count, point = sol()


print(count)
paths = deque()
paths.append(1)
while point!=n:
    paths.append(point)
    point = visited[point][1]
if n != 1:
    paths.append(n)

paths.reverse()
print(*paths)





