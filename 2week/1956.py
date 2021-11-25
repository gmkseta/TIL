# import sys
# import heapq


# V, E = list(map(int, sys.stdin.readline().split()))
# graph = {key: {} for key in range(1, E)}
# for i in range(E):
#     a, b, c = list(map(int, sys.stdin.readline().split()))
#     graph[a][b] = c


# def dijkstra(graph, start, end):
#     distances = {node: float('inf') for node in graph}
#     distances[start] = 0
#     queue = []
#     heapq.heappush(queue, [distances[start], start])

#     while queue:
#         current_distance, current_node = heapq.heappop(queue)
#         if distances[current_node] < current_distance:
#             continue
#         for adjacent, weight in graph[current_node].items():
#             distance = current_distance + weight

#             if distance < distances[adjacent]:
#                 distances[adjacent] = distance
#                 heapq.heappush(queue, [distance, adjacent])

#     return distances[end]


# result = float('inf')
# for i in graph.keys():
#     for j in graph[i].keys():
#         result = min(result, dijkstra(graph, j, i) + graph[i][j])

# print(result)

import sys

V, E = list(map(int, sys.stdin.readline().split()))
graph = [[float('inf')] * (V+1) for _ in range(V+1)]
for i in range(E):
    start, end, dist = list(map(int, sys.stdin.readline().split()))
    graph[start][end] = dist

for i in range(1, V+1):
    for j in range(1, V+1):
        if i == j:
            continue
        for k in range(1, V+1):
            if i == k:
                continue
            if graph[j][k] > graph[j][i] + graph[i][k]:
                graph[j][k] = graph[j][i] + graph[i][k]

result = float('inf')
for i in range(1, V+1):
    result = min(result, graph[i][i])
if result == float('inf'):
    print(-1)
else:
    print(result)
