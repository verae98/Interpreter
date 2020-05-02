import re
import os
from typing import List, Tuple, Callable, Union
from Enums import Error, Errornr

class Token():
    def __init__(self, instance : Tuple[str,str]): # ("PLUS", "+")
        self.instance = instance[0]
        self.type = instance[1]

    def __str__(self) -> str:
        return (self.instance + " -> " + self.type)

    def __repr__(self) -> str:
        return self.__str__()

def returnTupleFromString(stringToParse : str) -> (Tuple[str, str], Error):

    if (stringToParse == "+"):
        return (("PLUS", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "-"):
        return (("MIN", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "*"):
        return (("MULTIPLY", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "/"):
        return (("DEVIDED_BY", stringToParse),Error(Errornr.NO_ERROR))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return (("NUMBER", stringToParse), Error(Errornr.NO_ERROR))
    if(stringToParse == "if"):
        return (("IF", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "else"):
        return (("ELSE", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "="):
        return (("ASSIGN", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "while"):
        return (("WHILE", stringToParse), Error(Errornr.NO_ERROR))

    if (stringToParse == "=="):
        return (("EQUAL", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "!="):
        return (("NOTEQUAL", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == ">="):
        return (("GE", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "<="):
        return (("SE", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == ">"):
        return (("GREATER", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "<"):
        return (("SMALLER", stringToParse), Error(Errornr.NO_ERROR))

    if (stringToParse == ";"):
        return (("SEMICOLON", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "("):
        return (("LPAREN", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == ")"):
        return (("RPAREN", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "{"):
        return (("LBRACE", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "}"):
        return (("RBRACE", stringToParse), Error(Errornr.NO_ERROR))
    if (stringToParse == "print"):
        return (("PRINT", stringToParse), Error(Errornr.NO_ERROR))
    if (re.fullmatch("^[a-zA-Z_][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse), Error(Errornr.NO_ERROR))

    else:
        errormsg = "CANNOT DEFINE: " + "\"" + stringToParse + "\""
        return (("ERROR", errormsg), Error(Errornr.SYNTAX_ERROR, errormsg))


def fileToWordlist(string_file : str) -> List[str]:
    if(len(string_file) <= 0):
        return [""]
    head = string_file[0]
    tail = string_file[1:]
    current_wordlist = fileToWordlist(tail)
    if(head == ' ' or head == '\t' or head == '\n' or head == '\r'):
        current_wordlist = [""] + current_wordlist

    else:
        # update first word in the wordlist
        new_word = head + current_wordlist[0]
        current_wordlist[0] = new_word

    return current_wordlist

# TODO: implements map
def wordlistToTokens(f : Callable, wordlist : List[str]) -> (List[Tuple[str, str]], Error):
    if(len(wordlist) == 0):
        return [], Error(Errornr.NO_ERROR, "")
    head, *tail = wordlist
    currentTokenlist, errornr = wordlistToTokens(f,tail)
    # removes tabs /r or double spaces
    word_to_parse = head.strip()
    # if error has occured or word is empty, dont change anything
    if(errornr.nr != Errornr.NO_ERROR or len(word_to_parse) == 0):
        return currentTokenlist, errornr
    # parse word and retieve tuple and errornr
    new_tuple, errornr = f(word_to_parse)
    return (([Token(new_tuple)] + currentTokenlist), errornr)


def readFromFile(filename : str) -> Union[str, None]:
    if(os.access(filename, os.R_OK)):
        f = open(filename, "r")
        return f.read()
    return None

def lexer(filename : str) -> Union[Tuple[List[Token], Error], Tuple[None, Error]]:
    fileContainer = readFromFile(filename)
    if(fileContainer != None):
        wordlist = fileToWordlist(fileContainer)
        tokenlist, errornr = wordlistToTokens(returnTupleFromString, wordlist)
        return tokenlist, errornr
    return None, Error(Errornr.FileNotFoundError, "Cannot open " + filename)

