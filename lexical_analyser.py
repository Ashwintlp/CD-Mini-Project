import re
import io

keywords=["int","void","main","print"]

operators = { '=': 'Assignment Operator','+': 'Additon Operator', '-' : 'Substraction Operator', '/' : 'Division Operator', '*': 'Multiplication Operator'}
optr_keys = operators.keys()

symbols = {';':'semi_colon','{' : 'left_brace', '}':'right_brace', '(':'left_parenthesis',')':'right_parenthesis' ,'[':'left_sqbracket',']':'right_sqbracket'}
symbol_keys = symbols.keys()
 
the_ch = " "    
the_line = 1
token_list = []
error = [] 


#get the next character from the input file
def next_ch():

    global the_ch, the_line
    the_ch = input_file.read(1)
    if the_ch == '\n':
        the_line += 1
    return the_ch


#handle identifiers and numbers 
def identifier_or_number(line_no):
    
    text = ""
    while the_ch.isalnum() or the_ch == '_' or the_ch =='.':
        text += the_ch
        next_ch()
           
    if len(text) == 0:
        error_msg = "Unrecognized character "+the_ch+" found in line : "+str(line_no)
        error.append(error_msg)
        next_ch()
        return '' , '' , ''
    
    elif text in keywords:
        token_list.append(text)
        return line_no, text, "Keyword"

    elif text in re.findall('[_a-zA-Z][_a-zA-Z0-9]*',text):
        token_list.append('id')
        return line_no , text , 'Identifier'
    
    elif text in re.findall('[0-9]+[.]?[0-9]*',text):
        token_list.append('num')
        return line_no , text , 'Number'

    elif text not in re.findall('[_a-zA-Z ][_a-zA-Z0-9 ]*',text):
        error_msg=text+" is an invalid identifier found in line : "+str(line_no)
        error.append(error_msg)
        return '','',''


#return the next token type 
def getToken():

    while the_ch.isspace():
        next_ch()
 
    line_no = the_line
 
    if len(the_ch) == 0:
        token_list.append('$')
        return line_no, '$' , 'Enf_of_input'

    elif the_ch in symbol_keys:
        token = the_ch
        token_list.append(token)
        sym = symbols[token]
        next_ch()
        return line_no, token , sym

    elif the_ch in optr_keys:
        token = the_ch
        token_list.append(token)
        opr = operators[token]
        next_ch()
        return line_no, token , opr
    
    else:
        return identifier_or_number(line_no)
 

#opening input file 
f = open("input.txt", "r")
i = f.read()

program = re.sub('//.*?\n|/\*.*?\*/', '', i, flags=re.S) #removes all comment lines from input file 
input_file = io.StringIO(program) #converting string to file object

print("\nOutput of Lexical Analyser\n--------------------------\n")
print("%5s %7s %9s" % ("Line No.", "Token","Meaning"))
print("----------------------------")

while True:
    t = getToken()
    line  = t[0]
    token = t[1]
    meaning  = t[2]

    if token != '' and token != '$': 
        print("%5s  %9s  %-15s" % (line, token, meaning))
    elif token == '$':
        break

#display error msg if found any    
if len(error) != 0:
    print("\n\n-------------",len(error),"ERROR FOUND ---------------\n")
    for msg in error:
        print(msg)
    print("\n-------------------------------------------")
    exit(0)

print("\nThere are total",line,"lines in program")
print("Tokens:",token_list)