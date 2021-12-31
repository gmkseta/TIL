import sys
import bisect
input = sys.stdin.readline

N, M, K = list(map(int, input().split()))
cards = list(map(int, input().split()))
player_cards = list(map(int, input().split()))
cards.sort()

parent = list(range(M))

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]


def union(x, y):
    x_root = find(x)
    y_root = find(y)
    parent[x_root] = y_root


for i in player_cards:
    idx = bisect.bisect_right(cards, i)
    idx = find(idx)
    print(cards[idx])
    if idx < M - 1:
        union(idx, idx+1)
