import sys
from collections import deque
input = sys.stdin.readline
sys.setrecursionlimit(10 ** 6)
RED, BLUE = 1, -1
n = int(input())


def dfs(vertex, color):
    colors[vertex] = color

    for graph in graphs[vertex]:
        if colors[graph] == color or (colors[graph] == 0 and not dfs(graph, -color)):
            return False
    return True


for _ in range(n):
    V, E = list(map(int, input().split()))
    graphs = [[] for _ in range(V + 1)]
    colors = [0] * (V + 1)   # 색상 저장
    for _ in range(E):
        u, v = list(map(int, input().split()))
        graphs[u].append(v)
        graphs[v].append(u)

    for v in range(1, V + 1):
        if colors[v] == 0 and not dfs(v, RED):
            print("NO")
            break
        if v == V:
            print('YES')
