import sys

infix_notation = list(sys.stdin.readline().rstrip())

operands = []
operators = []

priorityOfOperators = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '(': 0,
}

result = []


for n in infix_notation:

    if 'A' <= n <= 'Z':
        result.append(n)
    else:
        if n == "(":
            operators.append(n)
        elif n == ")":
            while len(operators) and operators[-1] != '(':
                result.append(operators.pop())
            operators.pop()
        else:
            while len(operators) and priorityOfOperators[n] <= priorityOfOperators[operators[-1]]:
                result.append(operators.pop())
            operators.append(n)

result.extend(list(reversed(operators)))

print("".join(result))
