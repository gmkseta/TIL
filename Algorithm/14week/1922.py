import sys

input = sys.stdin.readline

N = int(input())

M = int(input())

mygraph = {
    'vertices': [i for i in range(1, N + 1)],
    'edges': [
        list(map(int, input().split())) for _ in range(M)
    ]
}

parent = dict()
rank = dict()


def find(node):
    # path compression 기법
    if parent[node] != node:
        parent[node] = find(parent[node])
    return parent[node]


def union(node_v, node_u):
    root1 = find(node_v)
    root2 = find(node_u)

    # union-by-rank 기법
    if rank[root1] > rank[root2]:
        parent[root2] = root1
    else:
        parent[root1] = root2
        if rank[root1] == rank[root2]:
            rank[root2] += 1


def make_set(node):
    parent[node] = node
    rank[node] = 0


def kruskal(graph):
    mst = list()

    # 1. 초기화
    for node in graph['vertices']:
        make_set(node)

    # 2. 간선 weight 기반 sorting
    edges = graph['edges']
    edges.sort(key=lambda x: x[2])

    # 3. 간선 연결 (사이클 없는)
    for edge in edges:
        node_v, node_u, weight = edge
        if find(node_v) != find(node_u):
            union(node_v, node_u)
            mst.append(edge)
    return sum(map(lambda x: x[2], mst))


print(kruskal(mygraph))
