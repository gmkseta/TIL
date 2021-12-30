import sys
input = sys.stdin.readline


M, N = list(map(int, input().split()))

dic = {}
for i in range(M):
    name = input().strip()
    dic[i] = name
    dic[name] = i

for _ in range(N):
    find = input().strip()
    if find.isdigit():
        print(dic[int(find)-1])
    else:
        print(dic[find]+1)

