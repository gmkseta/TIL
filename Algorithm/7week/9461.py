
import sys
input = sys.stdin.readline

t = int(input())


for _ in range(t):
  n = int(input())
  fibo=[1,1,1]  
  for i in range(3, n):
    fibo[0], fibo[1], fibo[2] = fibo[1], fibo[2], fibo[0]+fibo[1]
  print(fibo[-1])