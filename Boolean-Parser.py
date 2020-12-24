# BNF grammer is
# stmt -> ( stmt op stmt ) |  " term " | ' term '
# op -> and | or
stack = []
qr = None
ptr = None


def match():
    global ptr, qr, stack
    # correct case
    if len(stack) == 0 and ptr == len(qr):
        return
    # top of stack matched with cur_token
    elif qr[ptr] == stack[len(stack) - 1]:
        stack.pop()
        ptr += 1
    # top of stack is "term"
    elif stack[len(stack) - 1] == "term":
        stack.pop()
        qr[ptr] = (qr[ptr], "term")
        ptr += 1
    # non_terminal or error
    else:
        function_name = stack.pop()
        try:
            eval(function_name + "()")
        except:
            print(function_name)
            raiseException(function_name)


def stmt():
    global ptr, qr, stack
    if qr[ptr] == "(":
        stack.append(")")
        stack.append("stmt")
        stack.append("op")
        stack.append("stmt")
        stack.append("(")
    elif qr[ptr] == '"' or qr[ptr] == "'":
        stack.append(qr[ptr])
        stack.append("term")
        stack.append(qr[ptr])
    else:
        raiseException(qr[ptr])


def op():
    global ptr, qr, stack
    if qr[ptr] == "or" or qr[ptr] == "and":
        stack.append(qr[ptr])
    else:
        raiseException(qr[ptr])


def raiseException(ch):
    raise Exception("Syntax error!")


def prepareStack():
    stack = []
    stack.append("$")
    stack.append(")")
    stack.append("stmt")
    stack.append("op")
    stack.append("stmt")
    stack.append("(")
    return stack


def prepareQr(query):
    query = "( " + query + " )" + " $"
    query = query.split()
    return query


def checkSyntax(query):
    global qr, ptr, stack
    if len(query) == 0:
        return
    qr = prepareQr(query)
    ptr = 0
    stack = prepareStack()
    while len(stack) > 0:
        match()
    return qr


def run(query):
    query = checkSyntax(query)
    result = []
    for token in query:
        if token != "'" and token != '"' and token != "$":
            result.append(token)
    print(result)
    return result
