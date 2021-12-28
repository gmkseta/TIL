import sys

input = sys.stdin.readline

arr = [[[False] * 101 for _ in range(-50, 51)] for _ in range(-50, 51)]


def w(a, b, c):
    d_a, d_b, d_c = a + 50, b + 50, c + 50
    if arr[d_a][d_b][d_c] is not False:
        return arr[d_a][d_b][d_c]
    if a <= 0 or b <= 0 or c <= 0:
        arr[d_a][d_b][d_c] = 1
        return 1
    if a > 20 or b > 20 or c > 20:
        arr[d_a][d_b][d_c] = w(20, 20, 20)
        return arr[d_a][d_b][d_c]
    if a < b < c:
        arr[d_a][d_b][d_c] = w(a, b, c - 1) + w(a, b - 1, c - 1) - w(a, b - 1, c)
        return arr[d_a][d_b][d_c]
    arr[d_a][d_b][d_c] = w(a - 1, b, c) + w(a - 1, b - 1, c) + w(a - 1, b, c - 1) - w(a - 1, b - 1, c - 1)
    return arr[d_a][d_b][d_c]


while True:
    a, b, c = list(map(int, input().split()))
    if a == -1 and b == -1 and c == -1:
        break
    print("w({}, {}, {}) = {}".format(a, b, c, w(a, b, c)))
