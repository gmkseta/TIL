import sys
input = sys.stdin.readline

n = int(input())
arr = [int(x) for x in input().split()]
arr.sort()

tmp = float('inf')
ans = [0]*3

for i in range(n - 2):
    if i > 0 and arr[i] == arr[i -1]:
        continue
    left, right = i + 1, n - 1

    while left < right:
        sum = arr[i] + arr[left] + arr[right]

        if abs(sum) < abs(tmp):
            ans[0], ans[1], ans[2] = arr[i], arr[left], arr[right]
            tmp = sum

        if sum < 0:
            left += 1
        elif sum > 0:
            right -= 1
        else:
            print(arr[i], arr[left], arr[right])
            sys.exit(0)

for k in range(3):
    print(ans[k], end=' ')