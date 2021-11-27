import sys


n = int(sys.stdin.readline())

edged_count = int(sys.stdin.readline())

graph = {i: [] for i in range(1, n+1)}


for i in range(edged_count):
    start, end = list(map(int, sys.stdin.readline().split()))
    graph[start].append(end)
    graph[end].append(start)

queue = [1]
visited = []
while len(queue) > 0:
    node = queue.pop()
    if node not in visited:
        visited.append(node)
        queue.extend(graph[node])


print(len(visited)-1)
