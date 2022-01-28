import sys

input = sys.stdin.readline

n = int(input())

w_e = []
e_w = []
heights = []
top = 0
for _ in range(n):
    h = int(input())
    heights.append(h)
    if h > top:
        top = h
    w_e.append(top)

top = 0
heights.reverse()
for h in heights:
    if h > top:
        top = h
    e_w.append(top)

e_w.reverse()

for (w, e) in zip(w_e, e_w):
    print(w, e)
