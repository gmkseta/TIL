T = int(input())

# 1-  a e 모
# 2- i-1 * 모 + i-1 * 자 - aa ae ee ea ba be
# 3- aaa aae aee aea aba abe/ i-1 * 모 / baa bae bee bea / i - 2 * 모 + 자


for i in range(T):
    c, v, l = list(map(int, input().split()))
    dp =
    dp[0] = v
    dp[1] = v * (c + v)

    print(dp)
    print("Case #{}: {}".format(i + 1, dp[l - 1]))
