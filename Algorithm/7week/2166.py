import sys
input = sys.stdin.readline

n = int(input())


points = []
for _ in range(n):
    x, y = list(map(int, input().split()))
    points.append((x,y))
points.append(points[0])

ans = 0

for i in range(n):
    ans += (points[i][0]*points[i+1][1] - points[i][1]*points[i+1][0])

print(round(abs(ans)/2,1))
