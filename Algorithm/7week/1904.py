import sys
input = sys.stdin.readline

fibo1 = 1
fibo2 = 2
n = int(input())

while n > 2:
    fibo1, fibo2 = fibo2, (fibo1+fibo2)%15746
    n -= 1

if n == 1:
    print(1)
else:
    print(fibo2)

