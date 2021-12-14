import sys
from collections import deque


n = int(sys.stdin.readline())

opers = list(sys.stdin.readline().rstrip())

queue = deque()


operands = {}

for i in range(ord('A'), ord('A')+n):
    operands[chr(i)] = int(sys.stdin.readline())

for oper in opers:
    if 'A' <= oper <= 'Z':
        queue.append(operands[oper])
    else:
        b = queue.pop()
        a = queue.pop()
        if oper == '+':
            queue.append(a+b)
        elif oper == '-':
            queue.append(a-b)
        elif oper == '*':
            queue.append(a*b)
        elif oper == '/':
            queue.append(a/b)


print("{:.2f}".format(queue.pop()))
