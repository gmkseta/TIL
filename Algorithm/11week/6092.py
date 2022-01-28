T = [0] * 1001
pow2 = [1] * 1001


def move(n, r):
    if n == 1:
        return 1
    m = -1
    for k in range(1, n):
        if n - k >= 63:
            continue
        if T[k]:
            kVal = T[k]
        else:
            T[k] = move(k, r)
            kVal = T[k]
        nkVal = pow2[n - k] - 1
        x = 2 * kVal + nkVal
        if m == -1 or x < m:
            m = x
    return m


pow2[0] = 1
for i in range(1, 1001):
    pow2[i] = pow2[i - 1] * 2

for i in range(1, 13):
    print(move(i, 4), end=" ")
