

import sys

n = int(sys.stdin.readline())
coins = [list(sys.stdin.readline().rstrip()) for _ in range(n)]

result = n**2

for bit in range(1 << n):
    tmp = [coins[i][:] for i in range(n)]
    for i in range(n):
        if bit & (1 << i):
            for j in range(n):
                if tmp[i][j] == 'H':
                    tmp[i][j] = 'T'
                else:
                    tmp[i][j] = 'H'
    total = 0
    for i in range(n):
        count = 0
        for j in range(n):
            if tmp[j][i] == 'T':
                count += 1
        total += min(count, n-count)

    result = min(result, total)

print(result)
