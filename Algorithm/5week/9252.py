import sys
a = [0] + list(sys.stdin.readline().strip())
b = [0] + list(sys.stdin.readline().strip())

lcsdp = [[""] * len(b) for i in range(len(a))]
for i in range(1, len(a)):
    for j in range(1, len(b)):
        if a[i] == b[j]:
            lcsdp[i][j] = lcsdp[i - 1][j - 1] + a[i]
        else:
            if len(lcsdp[i - 1][j]) > len(lcsdp[i][j - 1]):
                lcsdp[i][j] = lcsdp[i - 1][j]
            else:
                lcsdp[i][j] = lcsdp[i][j - 1]
print(len(lcsdp[len(a) - 1][len(b) - 1]))
print(lcsdp[len(a) - 1][len(b) - 1])


# N = int(sys.stdin.readline())
# source = list(map(int, sys.stdin.readline().split()))
# M = int(sys.stdin.readline())
# target = list(map(int, sys.stdin.readline().split()))

# result = {k: 0 for k in target}

# for i in source:
#     if i in result.keys():
#         result[i] += 1

# print(*list(map(lambda x: result[x], target)))
