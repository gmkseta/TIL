import sys

N, K = map(int, sys.stdin.readline().split())

s = [[0] * 201 for i in range(201)]

for i in range(201):
    s[i][1] = 1

for i in range(1, 201):
    for j in range(201):
        for l in range(j + 1):
            s[j][i] += s[l][i - 1]


print(s[N][K] % 1000000000)
