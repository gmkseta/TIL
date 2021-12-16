import sys


n = int(sys.stdin.readline())


def operate(number):
    # D S L R
    return (2*number) % 10000, 9999 if number == 0 else number - 1, (number % 1000)*10 + number//1000, number // 10 + (number % 10)*1000


def bfs(start, end):
    visited = [0]*10_000
    need_visited = [('', start)]
    while need_visited:
        node = need_visited.pop(0)
        dn, sn, ln, rn = operate(node[1])
        d_path, s_path, l_path, r_path = node[0] + \
            'D', node[0]+'S', node[0]+'L', node[0]+'R'
        if dn == end:
            return d_path
        elif sn == end:
            return s_path
        elif ln == end:
            return l_path
        elif rn == end:
            return r_path
        else:
            if visited[dn] == 0:
                visited[dn] = 1
                need_visited.append((d_path, dn))
            if visited[sn] == 0:
                visited[sn] = 1
                need_visited.append((s_path, sn))
            if visited[ln] == 0:
                visited[ln] = 1
                need_visited.append((l_path, ln))
            if visited[rn] == 0:
                visited[rn] = 1
                need_visited.append((r_path, rn))


for j in range(n):

    start, end = list(map(int, sys.stdin.readline().split()))
    print(bfs(start, end))
