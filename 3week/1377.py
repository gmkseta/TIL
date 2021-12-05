import sys
import bisect


n = int(sys.stdin.readline().rstrip())

numbers = []
for i in range(n):
    number = int(sys.stdin.readline().rstrip())
    numbers.append((number, i))

sorted_numbers = sorted(numbers)

result = 0

for i in range(n):
    result = max(
        sorted_numbers[i][1] - i + 1,
        result
    )

print(result)
