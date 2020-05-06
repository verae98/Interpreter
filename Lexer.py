import re
import os
import io
from typing import List, Tuple, Callable, Union, TypeVar
from Enums import Error, Errornr

class Token():
    def __init__(self, instance : Tuple[str,str, int]): # ("PLUS", "+")
        self.instance = instance[0]
        self.type = instance[1]
        self.linenr = instance[2]

    def __str__(self) -> str:
        return (self.instance + " -> " + self.type)

    def __repr__(self) -> str:
        return self.__str__()

def new_returnTupleFromString(stringToParse : str, linenr : int) -> (Tuple[str, str, int]):
    if (stringToParse == "mas"):
        return (("PLUS", stringToParse, linenr))
    if (stringToParse == "eksi"):
        return (("MIN", stringToParse, linenr))
    if (stringToParse == "vezes"):
        return (("MULTIPLY", stringToParse, linenr))
    if (stringToParse == "dela"):
        return (("DEVIDED_BY", stringToParse, linenr))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return (("NUMBER", stringToParse, linenr))
    if(stringToParse == "ef"):
        return (("IF", stringToParse, linenr))
    if (stringToParse == "annars"):
        return (("ELSE", stringToParse, linenr))
    if (stringToParse == "er"):
        return (("ASSIGN", stringToParse, linenr))
    if (stringToParse == "aika"):
        return (("WHILE", stringToParse, linenr))

    if (stringToParse == "lig"):
        return (("EQUAL", stringToParse, linenr))
    if (stringToParse == "unterschiedlich"):
        return (("NOTEQUAL", stringToParse, linenr))
    if (stringToParse == ">="):
        return (("GE", stringToParse, linenr))
    if (stringToParse == "<="):
        return (("SE", stringToParse, linenr))
    if (stringToParse == ">"):
        return (("GREATER", stringToParse, linenr))
    if (stringToParse == "<"):
        return (("SMALLER", stringToParse, linenr))

    if (stringToParse == "fin"):
        return (("SEMICOLON", stringToParse, linenr))
    if (stringToParse == "haakje_begin"):
        return (("LPAREN", stringToParse, linenr))
    if (stringToParse == "haakje_eind"):
        return (("RPAREN", stringToParse, linenr))
    if (stringToParse == "fa_inizio"):
        return (("LBRACE", stringToParse, linenr))
    if (stringToParse == "fa_fine"):
        return (("RBRACE", stringToParse, linenr))
    if (stringToParse == "print"):
        return (("PRINT", stringToParse, linenr))
    if (re.fullmatch("^[@][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse, linenr))

    else:
        return (("ERROR", stringToParse, linenr))

def returnTupleFromString(stringToParse : str, linenr : int) -> (Tuple[str, str, int]):

    if (stringToParse == "+"):
        return (("PLUS", stringToParse, linenr))
    if (stringToParse == "-"):
        return (("MIN", stringToParse, linenr))
    if (stringToParse == "*"):
        return (("MULTIPLY", stringToParse, linenr))
    if (stringToParse == "/"):
        return (("DEVIDED_BY", stringToParse, linenr))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return (("NUMBER", stringToParse, linenr))
    if(stringToParse == "if"):
        return (("IF", stringToParse, linenr))
    if (stringToParse == "else"):
        return (("ELSE", stringToParse, linenr))
    if (stringToParse == "="):
        return (("ASSIGN", stringToParse, linenr))
    if (stringToParse == "while"):
        return (("WHILE", stringToParse, linenr))

    if (stringToParse == "=="):
        return (("EQUAL", stringToParse, linenr))
    if (stringToParse == "!="):
        return (("NOTEQUAL", stringToParse, linenr))
    if (stringToParse == ">="):
        return (("GE", stringToParse, linenr))
    if (stringToParse == "<="):
        return (("SE", stringToParse, linenr))
    if (stringToParse == ">"):
        return (("GREATER", stringToParse, linenr))
    if (stringToParse == "<"):
        return (("SMALLER", stringToParse, linenr))

    if (stringToParse == ";"):
        return (("SEMICOLON", stringToParse, linenr))
    if (stringToParse == "("):
        return (("LPAREN", stringToParse, linenr))
    if (stringToParse == ")"):
        return (("RPAREN", stringToParse, linenr))
    if (stringToParse == "{"):
        return (("LBRACE", stringToParse, linenr))
    if (stringToParse == "}"):
        return (("RBRACE", stringToParse, linenr))
    if (stringToParse == "print"):
        return (("PRINT", stringToParse, linenr))
    if (re.fullmatch("^[a-zA-Z_][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse, linenr))

    else:
        return (("ERROR", stringToParse, linenr))

def fileToWordlist(string_file : str) -> List[str]:
    wordlist = createWordlist(string_file)
    # filter empty characters
    wordlist = list(filter((lambda x: x != ''), wordlist))
    return wordlist

def createWordlist(string_file : str) -> List[str]:
    if(len(string_file) <= 0):
        return [""]
    head = string_file[0]
    tail = string_file[1:]
    current_wordlist = createWordlist(tail)
    # split word when one of those tokens appear
    if(head == ' ' or head == '\t' or head == '\n' or head == '\r'):
        current_wordlist = [""] + current_wordlist

    else:
        # update first word in the wordlist
        new_word = head + current_wordlist[0]
        current_wordlist[0] = new_word

    return current_wordlist

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def foldl(f: Callable[[A, B], C], base : B, list : List[A]) -> List[C]:
    if(len(list) == 0):
        return base
    head, *tail = list
    return (f(head, foldl(f, base, tail)))

A = TypeVar('A')
B = TypeVar('B')
def wordlistToTokens(f : Callable [[A, B], Token], wordlist : List[str], linenr : int) -> (List[Token]):
    line_list = [linenr] * len(wordlist)
    string_and_line = list((zip(wordlist,line_list)))
    tokenlist = foldl(f,[], (string_and_line))
    return tokenlist

def read_rec(f : io.TextIOWrapper) -> List[str]:
    read = (f.readline())
    if (read == ""):
        return [read]
    # check if line is comment
    if(read[0] == "$"):
        return read_rec(f)
    return [read] + read_rec(f)

def readFromFile(filename : str) -> Union[List[str], None]:
    if(os.access(filename, os.R_OK)):
        f = open(filename, "r")
        lines = read_rec(f)
        f.close()
        return lines
    return None

def function_wordToTuple(x : Tuple[str,int], tail : List[Token]) -> List[Token]:
    return [Token(returnTupleFromString(x[0], x[1]))] + tail

def lex_func(head : str, linenr : int) -> List[Token]:
    wordlist = fileToWordlist(head)
    tokenlist = wordlistToTokens(function_wordToTuple, wordlist, linenr)
    return tokenlist

def lex_rec(f : Callable[[str,int], List[Token]], fileContainer : List[str]) -> List[Token]:
    if(len(fileContainer) <= 0):
        return []
    return lex_rec(f, fileContainer[:-1]) + f(fileContainer[-1], len(fileContainer))

def lexer(filename : str) -> Union[Tuple[List[Token], Error], Tuple[None, Error]]:
    fileContainer = readFromFile(filename)
    if(fileContainer != None):
        tokenlist = lex_rec(lex_func, fileContainer)
        errorlist = list(filter(lambda x: x.instance == "ERROR", tokenlist))
        error = Error(Errornr.NO_ERROR)
        if (len(errorlist) > 0):
            error = (Error(Errornr.SYNTAX_ERROR, "Cannot define " + " \"" + errorlist[0].type + "\" " + " "))
        return tokenlist, error
    return None, Error(Errornr.FileNotFoundError, "Cannot open " + filename)

