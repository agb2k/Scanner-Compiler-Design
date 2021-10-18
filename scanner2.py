# from nltk.tokenize import sent_tokenize
#
# # Allows the user to select the filename they would like to scan
# print("Enter Filename: ")
# file = input()
#
# # Opens the file selected by the user
# f = open(file, "r", encoding='utf-8')
# code = f.read().split()
# print(code)
#
# for x in code:
#     print(sent_tokenize(x))

import tokenize

with open('prog1.py', 'rb') as f:
    tokens = tokenize.tokenize(f.readline)
    for token in tokens:
        print(token)
