import sys


n = int(sys.stdin.readline())
counter = 0
for _ in range(n):

    string = list(sys.stdin.readline().rstrip())
    current_char = string[0]
    existed = set()
    existed.add(current_char)
    is_group_word = True
    for i in string[1:]:
        if i != current_char:
            if i in existed:
                is_group_word = False
                break
            else:
                existed.add(i)
        current_char = i
    if is_group_word:
        counter += 1


print(counter)
