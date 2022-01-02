import sys 
from collections import deque
input = sys.stdin.readline 
N, M = map(int, input().split()) 

dp = [0]*(N+1)

graph = [[] for _ in range(N+1)]
queue = deque() 
arr = [list(map(int, input().split())) for _ in range(M)]

for a, b in arr: 
    dp[b] += 1 
    graph[a].append(b) 
for i in range(1, N + 1): 
  if dp[i] == 0: 
    queue.append(i) 

while queue: 
  student = queue.popleft()
  for j in graph[student]: 
    dp[j] -= 1 
    if dp[j] == 0: 
      queue.append(j) 
  print(student, end = ' ')

