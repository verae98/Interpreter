import re
import os
from typing import List, Tuple, Callable, Union
from Enums import Error, Errornr
from functools import reduce

class Token():
    def __init__(self, instance : Tuple[str,str]): # ("PLUS", "+")
        self.instance = instance[0]
        self.type = instance[1]

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

def returnTupleFromString(stringToParse : str) -> (Tuple[str, str]):

    if (stringToParse == "+"):
        return (("PLUS", stringToParse))
    if (stringToParse == "-"):
        return (("MIN", stringToParse))
    if (stringToParse == "*"):
        return (("MULTIPLY", stringToParse))
    if (stringToParse == "/"):
        return (("DEVIDED_BY", stringToParse))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return (("NUMBER", stringToParse))
    if(stringToParse == "if"):
        return (("IF", stringToParse))
    if (stringToParse == "else"):
        return (("ELSE", stringToParse))
    if (stringToParse == "="):
        return (("ASSIGN", stringToParse))
    if (stringToParse == "while"):
        return (("WHILE", stringToParse))

    if (stringToParse == "=="):
        return (("EQUAL", stringToParse))
    if (stringToParse == "!="):
        return (("NOTEQUAL", stringToParse))
    if (stringToParse == ">="):
        return (("GE", stringToParse))
    if (stringToParse == "<="):
        return (("SE", stringToParse))
    if (stringToParse == ">"):
        return (("GREATER", stringToParse))
    if (stringToParse == "<"):
        return (("SMALLER", stringToParse))

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

def wordlistToTokens(f : Callable, wordlist : List[str]) -> (List[Tuple[str, str]], Error):
    error = Error(Errornr.NO_ERROR)
    reduce_list = foldl(f, [], wordlist)
    errorlist = list(filter(lambda x: x.instance == "ERROR", reduce_list))
    if(len(errorlist) > 0):
        text = "Cannot define " + " \"" + errorlist[0].type + "\" " +  " "
        error = Error(Errornr.SYNTAX_ERROR, text)
    return (reduce_list, error)

def readFromFile(filename : str) -> Union[str, None]:
    if(os.access(filename, os.R_OK)):
        f = open(filename, "r")
        return f.read()
    return None

def function_wordToTuple(x, tail):
    return [Token(returnTupleFromString(x))] + tail

def lexer(filename : str) -> Union[Tuple[List[Token], Error], Tuple[None, Error]]:
    fileContainer = readFromFile(filename)
    if(fileContainer != None):
        wordlist = fileToWordlist(fileContainer)
        tokenlist, error = wordlistToTokens(function_wordToTuple, wordlist)
        return tokenlist, error
    return None, Error(Errornr.FileNotFoundError, "Cannot open " + filename)

