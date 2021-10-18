# Scanner Implemented with re module

import re

# Allows the user to select the filename they would like to scan
print("Enter Filename: ")
file = input()

# Opens the file selected by the user
f = open(file, "r", encoding='utf-8')
code = f.read()

# Get rid of comments
# tokenList = re.split("#.+", code)

# Splits up tokens and puts into list
tokenList = list(filter(None, re.split(r"(?=')('[^'\\]*')|\s+|([(),:])", code)))

# If between string " or ' ,
for x in tokenList:
    if re.search(r"^(\d+(?:\.\d+)?)$", x):
        print(f"(number, \'{x}\')")
    elif re.search(r"^(<=|<|>|=|>=|!=|==|!|\*|\\|%|\+|-)$", x):
        print(f"(operator, \'{x}\')")
    elif re.search(r'^(def|if|return|elif|else|for|in)$', x):
        print(f"(reserved, \'{x}\')")
    elif re.search(r"^([)(:,])$", x):
        print(f"(symbols, \'{x}\')")
    elif re.search(r"^(?=')('[^'\\]*')$", x):
        print(f"(string, {x})")
    else:
        print(f"(UNKNOWN, \'{x}\')")

print(len(tokenList))
