import re
from typing import List, Tuple

def returnTupleFromString(stringToParse : str) -> Tuple[str, str]:
    if (stringToParse == "+"):
        return (("PLUS", stringToParse))
    if (stringToParse == "-"):
        return (("MIN", stringToParse))
    if (stringToParse.isnumeric()):
        return (("NUMBER", stringToParse))
    if(stringToParse == "if"):
        return (("IF", stringToParse))
    if (stringToParse == "else"):
        return (("ELSE", stringToParse))
    if (stringToParse == ""):
        return (("EQUAL", stringToParse))
    if (stringToParse == ";"):
        return (("SEMICOLON", stringToParse))
    if (stringToParse == "("):
        return (("LPAREN", stringToParse))
    if (stringToParse == ")"):
        return (("RPAREN", stringToParse))
    if (stringToParse == "{"):
        return (("LBRACE", stringToParse))
    if (stringToParse == "}"):
        return (("RBRACE", stringToParse))
    if (stringToParse == "print"):
        return (("PRINT", stringToParse))
    if (re.fullmatch("^[a-zA-Z_][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse))

    else:
        errormsg = "CANNOT DEFINE: " + stringToParse
        return ("ERROR", errormsg)


def fileToWordlist(string_file : str) -> List[str]:
    if(len(string_file) <= 0):
        return [""]
    current_wordlist = fileToWordlist(string_file[1:])
    if(string_file[0] == ' ' or string_file[0] == '\t' or string_file == '\n'):
        current_wordlist = [""] + current_wordlist

    else:
        new_word = string_file[0] + current_wordlist[0]
        current_wordlist[0] = new_word

    return current_wordlist

def wordlistToTokens(wordlist : List[str]) -> List[Tuple[str, str]]:
    if(len(wordlist) == 0):
        return []
    currentTokenlist = wordlistToTokens(wordlist[1:])
    new_tuple = returnTupleFromString(wordlist[0])
    return ([Token(new_tuple)] + currentTokenlist)

def readFromFile(filename : str) -> str:
    f = open(filename, "r")
    return f.read()

def lexer(filename):
    wordlist = fileToWordlist(readFromFile(filename))
    tokenlist = wordlistToTokens(wordlist)
    return tokenlist

class Token():
    def __init__(self, instance : Tuple[str,str]): # ("PLUS", "+")
        self.instance = instance[0]
        self.type = instance[1]

    def __str__(self):
        return (self.instance + " -> " + self.type)

    def __repr__(self):
        return self.__str__()