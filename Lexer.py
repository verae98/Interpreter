import re
import os
from typing import List, Tuple, Callable, Union
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

def new_returnTupleFromString(stringToParse : str) -> (Tuple[str, str]):
    if (stringToParse == "mas"):
        return (("PLUS", stringToParse))
    if (stringToParse == "eksi"):
        return (("MIN", stringToParse))
    if (stringToParse == "vezes"):
        return (("MULTIPLY", stringToParse))
    if (stringToParse == "dela"):
        return (("DEVIDED_BY", stringToParse))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return (("NUMBER", stringToParse))
    if(stringToParse == "ef"):
        return (("IF", stringToParse))
    if (stringToParse == "annars"):
        return (("ELSE", stringToParse))
    if (stringToParse == "er"):
        return (("ASSIGN", stringToParse))
    if (stringToParse == "aika"):
        return (("WHILE", stringToParse))

    if (stringToParse == "lig"):
        return (("EQUAL", stringToParse))
    if (stringToParse == "unterschiedlich"):
        return (("NOTEQUAL", stringToParse))
    if (stringToParse == ">="):
        return (("GE", stringToParse))
    if (stringToParse == "<="):
        return (("SE", stringToParse))
    if (stringToParse == ">"):
        return (("GREATER", stringToParse))
    if (stringToParse == "<"):
        return (("SMALLER", stringToParse))

    if (stringToParse == "fin"):
        return (("SEMICOLON", stringToParse))
    if (stringToParse == "haakje_begin"):
        return (("LPAREN", stringToParse))
    if (stringToParse == "haakje_eind"):
        return (("RPAREN", stringToParse))
    if (stringToParse == "fa_inizio"):
        return (("LBRACE", stringToParse))
    if (stringToParse == "fa_fine"):
        return (("RBRACE", stringToParse))
    if (stringToParse == "print"):
        return (("PRINT", stringToParse))
    if (re.fullmatch("^[@][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse))

    else:
        return (("ERROR", stringToParse))

def returnTupleFromString(stringToParse : str, linenr : int) -> (Tuple[str, str]):

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
        return (("ERROR", stringToParse))

def fileToWordlist(string_file : str) -> List[str]:
    wordlist = createWordlist(string_file)
    wordlist = filter((lambda x: x != ' ' and x != '\t' and x != '\n' and x != '\r' and x != ''), wordlist)
    wordlist = list(wordlist)
    return wordlist

def createWordlist(string_file : str) -> List[str]:
    if(len(string_file) <= 0):
        return [""]
    head = string_file[0]
    tail = string_file[1:]
    current_wordlist = createWordlist(tail)
    if(head == ' ' or head == '\t' or head == '\n' or head == '\r'):
        current_wordlist = [""] + current_wordlist

    else:
        # update first word in the wordlist
        new_word = head + current_wordlist[0]
        current_wordlist[0] = new_word

    return current_wordlist


def foldl(f: Callable, base, list):
    if(len(list) == 0):
        return base
    head, *tail = list
    return (f(head, foldl(f, base, tail)))

def wordlistToTokens(f : Callable, wordlist : List[str], linenr : int) -> (List[Tuple[str, str]], Error):
    error = Error(Errornr.NO_ERROR)
    line_list = [linenr] * len(wordlist)
    string_and_line = list((zip(wordlist,line_list)))
    tokenlist = foldl(f,[], (string_and_line))
    errorlist = list(filter(lambda x: x.instance == "ERROR", tokenlist))
    if(len(errorlist) > 0):
        text = "Cannot define " + " \"" + errorlist[0].type + "\" " +  " "
        error = Error(Errornr.SYNTAX_ERROR, text)
    return (tokenlist, error)

def read_rec(f):
    read = (f.readline())
    if (read == ""):
        return [read]
    return [read] + read_rec(f)

def readFromFile(filename : str) -> Union[str, None]:
    if(os.access(filename, os.R_OK)):
        f = open(filename, "r")
        lines = read_rec(f)
        f.close()
        return lines
    return None

def function_wordToTuple(x, tail):
    return [Token(returnTupleFromString(x[0], x[1]))] + tail

def lex_func(head, linenr : int):
    wordlist = fileToWordlist(head)
    tokenlist, error = wordlistToTokens(function_wordToTuple, wordlist, linenr)
    return tokenlist

def lex_rec(f : Callable, fileContainer) -> List[Token]:
    if(len(fileContainer) <= 0):
        return []
    return lex_rec(f, fileContainer[:-1]) + f(fileContainer[-1], len(fileContainer))

def lexer(filename : str) -> Union[Tuple[List[Token], Error], Tuple[None, Error]]:
    fileContainer = readFromFile(filename)
    if(fileContainer != None):
        tokenlist = lex_rec(lex_func, fileContainer)
        return tokenlist, Error(Errornr.NO_ERROR)
    return None, Error(Errornr.FileNotFoundError, "Cannot open " + filename)

