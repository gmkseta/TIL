T = int(input())

for i in range(T):
    c, v, l = list(map(int, input().split()))
    dp = [0] * l
    dp[0] = v
    dp[1] = v * (c + v)

    print(dp)
    print("Case #{}: {}".format(i + 1, dp[l - 1]))
