import sys
from bisect import bisect_left
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))
dp = [arr[0]]
record = [0]*n
record[0]=1
for i in range(1, n):
  idx = bisect_left(dp, arr[i])
  if idx == len(dp):
    dp.append(arr[i])
  else:
     dp[idx] = arr[i]
  record[i] = idx+1



ans = []
find_dp = len(dp)
for i in range(n-1,-1,-1):
  if record[i] == find_dp:
    ans.append(arr[i])
    find_dp -= 1
  if find_dp < 1:
    break
print(len(ans))
print(*ans[::-1])
    