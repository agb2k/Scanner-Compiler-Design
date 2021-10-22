# Scanner/Lexer Implemented with re library

import re

# Allows the user to input the filename they would like to scan
print("Enter Filename: ")
file = input()

# Reads the file selected by the user
f = open(file, "r", encoding='utf-8')
code = f.read()

# Splits up tokens and puts into list
# The regex code gets rid of whitespace and comments while keeping strings intact
tokenList = list(filter(None, re.split(r"(?=')('[^'\\]*')|#.+|\s+|([)(:,}{\[\]])", code)))

# Loops through entire list of tokens to
for x in tokenList:
    # Determines whether token is a number which is inclusive of floats and integers
    if re.search(r"^(\d+(?:\.\d+)?)$", x):
        print(f"(number, \'{x}\')")
    # Determines whether a token is one of the operators
    elif re.search(r"^(<=|<|>|=|>=|!=|==|!|\*|\\|%|\+|-)$", x):
        print(f"(operator, \'{x}\')")
    # Determines whether a token is a reserved keyword
    elif re.search(r'^(def|if|return|elif|else|for|in)$', x):
        print(f"(reserved, \'{x}\')")
    # Determines whether a token is a symbol
    elif re.search(r"^([)(:,}{\[\]])$", x):
        print(f"(symbol, \'{x}\')")
    # Determines whether a token is a string
    elif re.search(r"^(?=')('[^'\\]*')|^(?=\")(\"[^\"\\]*\")$", x):
        print(f"(string, {x})")
    # If other options are not possible token is identifier
    else:
        print(f"(identifier, \'{x}\')")

print(print(f"No. of Tokens: {len(tokenList)}"))