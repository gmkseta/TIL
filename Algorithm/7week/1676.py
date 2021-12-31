
import sys
input = sys.stdin.readline

n = int(input())

def get_count(n, i):
    result = 0
    while i%n == 0:
        result +=1
        i = i//n
    return result

two_counter = 0
five_counter = 0
for i in range(n, 0, -1):
    if i % 2 == 0:
        two_counter += get_count(2, i)
    if i % 5 == 0:
        five_counter += get_count(5, i)

print(min(two_counter, five_counter))
