

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def infix_to_postfix(infixexpr, prec):
    # prec = {}
    # prec["*"] = 3
    # prec["/"] = 3
    # prec["+"] = 2
    # prec["-"] = 2
    # prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token not in "()+-*/":
            postfixList.append(token)
        elif token == "(":
            opStack.push(token)
        elif token == ")":
            topToken = opStack.pop()
            while topToken != "(":
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def postfix_eval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token.isnumeric():
            operandStack.push(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = do_math(token, operand1, operand2)
            operandStack.push(result)
    return operandStack.pop()


def do_math(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


if __name__ == "__main__":
    with open("input.txt") as f:
        equations = [line.rstrip().replace("(", "( ").replace(")", " )") for line in f]
    
    prec_1 = {}
    prec_1["*"] = 2
    prec_1["/"] = 2
    prec_1["+"] = 2
    prec_1["-"] = 2
    prec_1["("] = 1

    equation_sum = 0
    for e in equations:
        e_postfix = infix_to_postfix(e, prec_1)
        e_evaluated = postfix_eval(e_postfix)
        equation_sum += e_evaluated
    print(f"Part 1: {equation_sum}")


    prec_2 = {}
    prec_2["*"] = 2
    prec_2["/"] = 2
    prec_2["+"] = 3
    prec_2["-"] = 3
    prec_2["("] = 1

    equation_sum_2 = 0
    for e in equations:
        e_postfix = infix_to_postfix(e, prec_2)
        e_evaluated = postfix_eval(e_postfix)
        equation_sum_2 += e_evaluated
    print(f"Part 2: {equation_sum_2}")
