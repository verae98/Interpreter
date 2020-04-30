import re
from typing import List, Tuple
from Enums import Error, Errornr

def returnTupleFromString(stringToParse : str) -> (Tuple[str, str], Error):

    if (stringToParse == "+"):
        return (("PLUS", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "-"):
        return (("MIN", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "*"):
        return (("MULTIPLY", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "/"):
        return (("DEVIDED_BY", stringToParse),Error(Errornr.NO_ERROR, ""))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return (("NUMBER", stringToParse), Error(Errornr.NO_ERROR, ""))
    if(stringToParse == "if"):
        return (("IF", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "else"):
        return (("ELSE", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "="):
        return (("ASSIGN", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "while"):
        return (("WHILE", stringToParse), Error(Errornr.NO_ERROR, ""))

    if (stringToParse == "=="):
        return (("EQUAL", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "!="):
        return (("NOTEQUAL", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == ">="):
        return (("GE", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "<="):
        return (("SE", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == ">"):
        return (("GREATER", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "<"):
        return (("SMALLER", stringToParse), Error(Errornr.NO_ERROR, ""))

    if (stringToParse == ";"):
        return (("SEMICOLON", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "("):
        return (("LPAREN", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == ")"):
        return (("RPAREN", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "{"):
        return (("LBRACE", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "}"):
        return (("RBRACE", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (stringToParse == "print"):
        return (("PRINT", stringToParse), Error(Errornr.NO_ERROR, ""))
    if (re.fullmatch("^[a-zA-Z_][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse), Error(Errornr.NO_ERROR, ""))

    else:
        errormsg = "CANNOT DEFINE: " + stringToParse
        return (("ERROR", errormsg), Error(Errornr.SYNTAX_ERROR, errormsg))


def fileToWordlist(string_file : str) -> List[str]:
    if(len(string_file) <= 0):
        return [""]
    current_wordlist = fileToWordlist(string_file[1:])
    if(string_file[0] == ' ' or string_file[0] == '\t' or string_file[0] == '\n' or string_file[0] == '\r'):
        current_wordlist = [""] + current_wordlist

    else:
        new_word = string_file[0] + current_wordlist[0]
        current_wordlist[0] = new_word

    return current_wordlist

def wordlistToTokens(wordlist : List[str]) -> (List[Tuple[str, str]], Error):
    if(len(wordlist) == 0):
        return [], Error(Errornr.NO_ERROR, "")
    currentTokenlist, errornr = wordlistToTokens(wordlist[1:])
    new_tuple = None
    if(errornr.nr == Errornr.NO_ERROR):
        word_to_parse = wordlist[0]

        # remove /n /r or double spaces
        word_to_parse = word_to_parse.strip()
        if(len(word_to_parse) == 0):
            return currentTokenlist, errornr

        new_tuple, errornr = returnTupleFromString(wordlist[0])
        return (([Token(new_tuple)] + currentTokenlist), errornr)
    return currentTokenlist, errornr

def readFromFile(filename : str) -> str:
    f = open(filename, "r")
    return f.read()

def lexer(filename):
    wordlist = fileToWordlist(readFromFile(filename))
    tokenlist, errornr = wordlistToTokens(wordlist)
    return tokenlist, errornr

class Token():
    def __init__(self, instance : Tuple[str,str]): # ("PLUS", "+")
        self.instance = instance[0]
        self.type = instance[1]

    def __str__(self):
        return (self.instance + " -> " + self.type)

    def __repr__(self):
        return self.__str__()