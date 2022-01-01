# import sys
# input = sys.stdin.readline


# def solution():
#     sudoku = [[*map(int, list(input().rstrip()))] for _ in range(9)]
#     rowset = [[True] * 10 for _ in range(9)]
#     colset = [[True] * 10 for _ in range(9)]
#     sqset = [[True] * 10 for _ in range(9)]
#     sq = [[0] * 9 for _ in range(9)]
#     cand = range(1, 10)

#     empty = []
#     for i in range(9):
#         for j in range(9):
#             sq[i][j] = (i // 3) * 3 + (j // 3)
#             num = sudoku[i][j]
#             if not num:
#                 empty.append((i, j))
#                 continue

#             rowset[i][num] = False
#             colset[j][num] = False
#             sqset[sq[i][j]][num] = False
#     empty_count = len(empty)

#     def dfs(cur):
#         if cur == empty_count:
#             return True

#         r, c = empty[cur]

#         rs = rowset[r]
#         cs = colset[c]
#         ss = sqset[sq[r][c]]
#         for num in cand:
#             if rs[num] and cs[num] and ss[num]:
#                 sudoku[r][c] = num
#                 rs[num] = cs[num] = ss[num] = False
#                 if dfs(cur + 1):
#                     return True
#                 sudoku[r][c] = 0
#                 rs[num] = cs[num] = ss[num] = True
#         return False

#     dfs(0)

#     return '\n'.join([''.join(map(str, sudoku[i])) for i in range(9)])


# print(solution())