from collections import deque

F, S, G, U, D = map(int, input().split())

need_visited = deque([[S, 0]])
visited = set()

ans = -1

while need_visited:
    cur, counter = need_visited.popleft()
    if not cur in visited:
        visited.add(cur)
        if cur == G:
            ans = counter
            break
        if cur + U <= F:
            need_visited.append([cur + U, counter + 1])

        if cur - D > 0:
            need_visited.append([cur - D, counter + 1])

if ans == -1:
    print('use the stairs')
else:
    print(ans)
