K = int(input())

ans = [1, 0]

for i in range(K):
    ans = [ans[1], ans[0] + ans[1]]

print(*ans)
