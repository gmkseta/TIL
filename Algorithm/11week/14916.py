n = int(input())

ans = -1
for i in range(n // 5, -1, -1):
    value = n - i * 5
    if value % 2 == 0:
        ans = (i + value // 2)
        break
print(ans)
