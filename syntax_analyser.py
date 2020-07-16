from lexical_analyser import * #import lexical analyser code

grammar = [
    ["S","R","main","(",")","{","C","}","$"],
    ["R","int","$"],
    ["R","void","$"],
    ["C","id","=","E",";","C","$"],
    ["C","print","(","id",")",";","C","$"],
    ["C","epsolon","$"],
    ["E","T","E'","$"],
    ["E'","+","T","E'","$"],
    ["E'","-","T","E'","$"],
    ["E'","epsolon","$"],
    ["T","F","T'","$"],
    ["T'","*","F","T'","$"],
    ["T'","/","F","T'","$"],
    ["T'","epsolon","$"],
    ["F","(","E",")","$"],
    ["F","{","E","}","$"],
    ["F","[","E","]","$"],
    ["F","id","$"],
    ["F","num","$"],
]

parsing_table = [
    ["S","int","0"],
    ["S","void","0"],
    ["R","int","1"],
    ["R","void","2"],
    ["C","print","4"],
    ["C","}","5"],
    ["C","id","3"],
    ["E","(","6"],
    ["E","{","6"],
    ["E","[","6"],
    ["E","id","6"],
    ["E","num","6"],
    ["E'","]","9"],
    ["E'","}","9"],
    ["E'",")","9"],
    ["E'","+","7"],
    ["E'","-","8"],
    ["E'",";","9"],
    ["T","(","10"],
    ["T","{","10"],
    ["T","[","10"],
    ["T","id","10"],
    ["T","num","10"],
    ["T'","]","13"],
    ["T'","}","13"],
    ["T'",")","13"],
    ["T'","+","13"],
    ["T'","-","13"],
    ["T'",";","13"],
    ["T'","*","11"],
    ["T'","/","12"],
    ["F","(","14"],
    ["F","{","15"],
    ["F","[","16"],
    ["F","id","17"],
    ["F","num","18"],
]

input_tokens = token_list #token_list is a set of all tokens from lexical analyser
ip = 0 
stack = ['S'] #Starting symbol S at top of stack
top = 0

def update_stack(x,s):
    global stack
    buffer = [] 
    print(grammar[x][0],"->",end="")
    y = 1

    while grammar[x][y] != '$':
        print(grammar[x][y],end="")

        if grammar[x][y] == 'epsolon':
            stack.pop()
            r = len(stack) - 1
            print("\n")
            return r

        buffer.append(grammar[x][y])
        y = y + 1

    stack.pop()
    for i in reversed(buffer):
        stack.append(i)
    r = len(stack) - 1
    print("\n")

    return r


print("\n\nOutput of Syntax Analyser(Parse Tree)\n-------------------------")

while input_tokens[ip] != '$':

    if top>-1:
        s = stack[top]
    t = input_tokens[ip]

    flag = False 

    for i in range(len(parsing_table)):

        if parsing_table[i][0] == s and parsing_table[i][1] == t:
            x = int(parsing_table[i][2])
            top = update_stack(x,s)
            flag = True
            break

        elif s == t:
            #print(t,"matched")
            ip = ip + 1
            stack.pop()
            top = top - 1
            flag = True
            break

    if flag == False:
        print("Syntax error found\nINVALID PROGRAM ")
        exit(1)

if len(stack) == 0: #if is stack empty then valid
    print("******* VALID PROGRAM *********")
else:
    print("Syntax error found\nINVALID PROGRAM ")
