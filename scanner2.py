# Scanner/Lexer built with NLTK library

from nltk.tokenize import word_tokenize

# Allows the user to select the filename they would like to scan
print("Enter Filename: ")
file = input()

# Opens the file selected by the user
f = open(file, "r", encoding='utf-8')
code = f.read()
tokens = word_tokenize(code)

# Deals with ' being separated due to NLTK
flg = False
for c, x in enumerate(tokens):
    # Conditional which checks if lexeme is a part of the string type
    if (not flg) and (x[0] == "\'") and (x[-1] != "\'"):
        text = x
        flg = True
        tokens[c] = ''
    # Conditional which checks whether lexeme is part of the content between apostrophes of string
    elif flg and x != "\'":
        text = text + x
        tokens[c] = ''
    # Conditional checks if lexeme is the end of a string
    elif flg and x == "\'":
        flg = False
        text = text + x
        tokens[c] = text
    else:
        continue

# Deals with certain operators like <= and >= being separated due to NLTK
for c, x in enumerate(tokens):
    # Conditional to check if lexemes are separated <= or >=
    if x == '=' and (tokens[c-1] == '<' or tokens[c-1] == '>'):
        tokens[c] = tokens[c-1] + x
        tokens[c-1] = ''

# Filters out empty strings
tokens = list(filter(None, tokens))
for x in tokens:
    # Conditional statement to test whether lexeme is reserved word
    if x == "def" or x == "if" or x == "return" or x == "elif" or x == "else" or x == "for" or x == "in":
        print(f"(reserved, \'{x}\')")
    # Conditional statement to test whether lexeme is reserved word
    elif x.isnumeric() or x.replace('.', '', 1).isdigit():
        print(f"(number, \'{x}\')")
    # Conditional statement to test whether lexeme is reserved word
    elif x == '>' or x == '<' or x == '>=' or x == '<=' or x == '==' or x == '&&' or x == '=' or x == '||' or x == '!' \
            or x == '%' or x == '*' or x == '\\' or x == '%' or x == '+' or x == '-':
        print(f"(operator, \'{x}\')")
    # Conditional statement to test whether lexeme is reserved word
    elif x == '(' or x == ')' or x == '[' or x == ']' or x == '{' or x == '}' or x == ':' or x == ',':
        print(f"(symbol, \'{x}\')")
    # Conditional statement to test whether lexeme is reserved word
    elif x[0] == '\'':
        print(f"(string, {x})")
    # Conditional statement to test whether lexeme is reserved word
    else:
        print(f"(identifier, \'{x}\')")
