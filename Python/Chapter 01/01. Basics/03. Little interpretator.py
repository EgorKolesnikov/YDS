## Egor Kolesnikov
##
## Interpretator to calculate mathematical expressions.
## Using reverse poland notation.
##

import sys
import collections


OPERATIONS = {'+', '-', '*', '/', '**'}
PRIORITY = {'(': 1, '+': 2, '-': 2, '*': 3, '/': 3, '**': 4}


def to_poland_notation(expression):
    stack = []
    poland_notation = []
    for token in expression:
        if(token == "("):
            stack.append(token)
        elif(token == ")"):
            while(stack[-1] != "("):
                top = stack.pop()
                poland_notation.append(top)
            stack.pop()
        elif(token in OPERATIONS):
            if(len(stack) == 0 or PRIORITY[stack[-1]] < PRIORITY[token]):
                stack.append(token)
                continue
            elif(PRIORITY[stack[-1]] >= PRIORITY[token]):
                while(stack and
                      PRIORITY[stack[-1]] >= PRIORITY[token]):
                    top = stack.pop()
                    poland_notation.append(top)
                stack.append(token)
        else:
            poland_notation.append(token)
    while(stack):
        poland_notation.append(stack.pop())
    return poland_notation


def calculate(expression):
    stack = []
    expression = to_poland_notation(expression)
    for token in expression:
        if(token in OPERATIONS):
            operand_2 = float(stack.pop())
            operand_1 = float(stack.pop())
            if(token == '+'):
                result = operand_1 + operand_2
            elif(token == '-'):
                result = operand_1 - operand_2
            elif(token == '*'):
                result = operand_1 * operand_2
            elif(token == '/'):
                result = operand_1 / operand_2
            elif(token == '**'):
                result = operand_1 ** operand_2
            stack.append(result)
        else:
            stack.append(token)
    answer = float(stack.pop())
    if(answer.is_integer()):
        print(int(answer))
    else:
        print(answer)
    return


expression = sys.stdin.readline()
if(expression[-1] == '\n'):
    expression = expression[:-1]
expression = expression.split(" ")
calculate(expression)

