import sys

input = sys.stdin.readline

n, k = list(map(int, input().split()))

coins = [int(input()) for _ in range(n)]

dp = [0] * (k + 1)


def
