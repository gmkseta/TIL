

# A, B = list(map(int, sys.stdin.readline().split()))


# dp = {}


# def make_dp(n):
#     if n % 2 == 1:
#         dp[n] = 0
#     elif n//2 not in dp:
#         make_dp(n//2)
#         dp[n] = dp[n//2]+1
#     else:
#         dp[n] = dp[n//2]+1


# result = 0
# for i in range(1, B+1):
#     make_dp(i)
#     result += 2**dp[i]

# for (x, y) in zip(dp.keys(), dp.values()):
#     print(2**y, end=" ")

# print(*dp.values())

# # # 1+2^1*n = x


# # # x/(1+2n)

# # 2 ^ k + 2 ^ (k+1) * n = x

# # 2^k(1+2n) = x

# # x/(1+2n)

# # num //


# # # 1+2*n = x


# # # 2 ^ 1 + 2 ^ 2 * n -> 1
# # # 2 ^ 2 + 2 ^ 3 * n -> 2
# # # 2 ^ 3 + 2 ^ 4 * n -> 3

# # # 2 ^ 0 + 2 ^ 1 * n = k


# # def getMaxN(n):
# #     counter = 0
# #     while n > 1:
# #         n = n//2
# #         counter += 1
# #     return counter


# # # maxN = getMaxN(B)


# # # def getValue(n):
# # #     for i in range(maxN, 0, -1):
# # #         if n % (2**(i+1)) == 2**i:
# # #             return i
# # #     return 0


# # # result = 0
# # # for i in range(A, B+1):
# # #     result += 2**getValue(i)

# # # print(result)


# # def func(num):
import sys
A, B = list(map(int, sys.stdin.readline().split()))


def f(n):
    if n <= 1:
        return n
    return n//2 + 2*f(n//2) + n % 2


print(f(B)-f(A-1))
