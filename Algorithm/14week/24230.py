import sys

input = sys.stdin.readline

N = int(input())

colors = [0] + list(map(int, input().split()))

ans = 0 if colors[1] == 0 else 1

for i in range(N - 1):
    a, b = sorted(list(map(int, input().split())))
    if colors[a] != colors[b]:
        ans += 1

print(ans)
