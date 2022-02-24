import sys
import math

input = sys.stdin.readline

H, Y = list(map(int, input().split()))

result = [0] * (Y + 1)
result[0] = H
rates = {5: 1.35, 3: 1.2, 1: 1.05}

for i in range(Y + 1):
    for year, rate in rates.items():
        if i - year >= 0:
            result[i] = max(result[i], math.floor(result[i - year] * rate))

print(result[-1])
