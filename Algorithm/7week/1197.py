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
    edges.sort()
    
    # 3. 간선 연결 (사이클 없는)
    for edge in edges:
        weight, node_v, node_u = edge
        if find(node_v) != find(node_u):
            union(node_v, node_u)
            mst.append(edge)
    
    return mst
  
import sys
input = sys.stdin.readline


V, E = list(map(int, input().split()))

mygraph = {
  'vertices': [i for i in range(1,V+1)],
  'edges': []
}
for _ in range(E):
  A,B,C = list(map(int, input().split()))
  mygraph['edges'].append((C,A,B))

result = kruskal(mygraph)
ans = 0
max_v = -float('inf')
for (v,_,_) in result:
  ans+=v
  max_v = max(v, max_v)
print(ans - max_v)