import sys
input = sys.stdin.readline

S = set()
operators = {
    "add": S.add,
    "remove": S.discard,
    "check": lambda x: print(1 if x in S else 0),
    "toggle": lambda x: S.remove(x) if x in S else S.add(x),
    "empty": lambda _: S.clear(),
    "all": lambda _: S.update([i for i in range(1, 21)])
}

n = int(input())

for _ in range(n):
    arg = input().strip().split()
    operators[arg[0]](arg[-1])

