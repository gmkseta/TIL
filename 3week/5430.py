import sys
import re

test_case = int(sys.stdin.readline())
pattern = re.compile("[0-9]+")
for _ in range(test_case):
    p = sys.stdin.readline().rstrip()
    n = int(sys.stdin.readline())
    arr = pattern.findall(sys.stdin.readline().rstrip())
    reverse_flag = False
    if n != len(arr):
        print("error")
    else:
        try:
            for i in p:
                if i == 'R':
                    reverse_flag = not reverse_flag
                elif i == 'D':
                    arr.pop(-1 if reverse_flag else 0)
            if reverse_flag:
                print('[', ','.join(list(reversed(arr))), ']', sep="")
            else:
                print('[', ','.join(arr), ']', sep="")
        except:
            print('error')
