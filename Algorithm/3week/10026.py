import sys

n = int(sys.stdin.readline())

table = []
for i in range(n):
    table.extend(list(sys.stdin.readline().rstrip()))


visited = [False] * n*n


def get_adj_idx(idx, color):
    result = []
    top = idx - n
    left = idx - 1
    right = idx + 1
    bottom = idx + n
    if top >= 0 and table[top] == color:
        result.append(top)
    if bottom < n*n and table[bottom] == color:
        result.append(bottom)
    if idx % n != 0 and table[left] == color:
        result.append(left)
    if idx % n != n-1 and table[right] == color:
        result.append(right)
    return result


def find_group(start_node):
    visited_idx = []
    need_visited = [start_node]
    while need_visited:
        node = need_visited.pop()
        if not visited[node]:
            visited[node] = True
            visited_idx.append(node)
            need_visited.extend(get_adj_idx(node, table[node]))
    return visited_idx


result = []

common_counter = 0

while not all(visited):
    find_group(visited.index(False))
    common_counter += 1

visited = [False] * n*n


counter = 0

table = ['G' if x == 'R' else x for x in table]
while not all(visited):
    find_group(visited.index(False))
    counter += 1

print(common_counter, counter)
