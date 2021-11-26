import sys


n = int(sys.stdin.readline())


for _ in range(n):
    queue = []
    gaulho = list(sys.stdin.readline().rstrip())
    result = "YES"
    for i in gaulho:
        if i == "(":
            queue.append(True)
        else:
            if len(queue) == 0:
                result = "NO"
                break
            queue.pop()
    if len(queue) != 0:
        result = "NO"
    print(result)
