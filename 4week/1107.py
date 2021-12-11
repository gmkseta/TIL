import sys


N = int(sys.stdin.readline().rstrip())
M = int(sys.stdin.readline())

if M > 0:
    broken = set(map(int, sys.stdin.readline().rstrip().split()))
else:
    broken = set()


near_number = float('inf')
for number in range(1_000_000):
    if set(map(int, str(number))) & broken:
        pass
    else:
        if abs(N-near_number) < abs(N-number):
            break
        if abs(N-near_number) > abs(N-number):
            near_number = number

result = abs(N-near_number) + len(str(near_number))
result = min(result, abs(N-100))
print(result)
