import sys
input = sys.stdin.readline

n = int(input())

board = []

parent = dict()
rank = dict()

def find(node):
  if parent[node] != node:
    parent[node] = find(parent[node])
  return parent[node]

def union(node_v, node_u):
  root1 = find(node_v)
  root2 = find(node_u)
  if rank[root1] > rank[root2]:
    parent[root2] = root1
  else:
    parent[root1] = root2
    if rank[root1] == rank[root2]:
      rank[root2]+=1

def make_set(node):
  parent[node]=node
  rank[node]=0  


def kruskal():
  result = 0
  for node in range(n):
    make_set(node)
  edges.sort()
  for edge in edges:
    weight, node_v, node_u = edge
    if find(node_v) != find(node_u):
      union(node_v, node_u)
      result+=weight
  return result
  
  
  

points = [list(map(float, input().split())) for _ in range(n)]
edges = []
get_dist = lambda a,b: ((a[0]-b[0])**2+(a[1]-b[1])**2)**(1/2)
for i in range(1, n):
  for j in range(0, i):
    edges.append((get_dist(points[i], points[j]), i, j))
    
  
print(kruskal())