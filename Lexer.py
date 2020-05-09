import re
import os
import io
from typing import List, Tuple, Callable, Union, TypeVar
from Enums import Error, Errornr, TokenValues

class Token():
    def __init__(self, instance : Tuple[TokenValues,str, int]): # ("PLUS", "+", 1)
        self.instance = instance[0]
        self.type = instance[1]
        self.linenr = instance[2]

    def __str__(self) -> str:
        return (str(self.instance.value) + " -> " + self.type)

    def __repr__(self) -> str:
        return self.__str__()

#returnTupleFromString :: srt -> int -> Tuple[str, str, int]
def returnTupleFromString(stringToParse : str, linenr : int) -> (Tuple[str, str, int]):
    """Checks string and returns corresponding tuple"""
    if (stringToParse == "mas"):
        return ((TokenValues.PLUS, stringToParse, linenr))
    if (stringToParse == "eksi"):
        return ((TokenValues.MIN, stringToParse, linenr))
    if (stringToParse == "vezes"):
        return ((TokenValues.MULTIPLY, stringToParse, linenr))
    if (stringToParse == "dela"):
        return ((TokenValues.DIVIDED_BY, stringToParse, linenr))
    if (stringToParse.isnumeric() or (stringToParse[0] == "-" and stringToParse[1:].isnumeric())):
        return ((TokenValues.NUMBER, stringToParse, linenr))
    if(stringToParse == "ef"):
        return ((TokenValues.IF, stringToParse, linenr))
    if (stringToParse == "annars"):
        return ((TokenValues.ELSE, stringToParse, linenr))
    if (stringToParse == "er"):
        return ((TokenValues.ASSIGN, stringToParse, linenr))
    if (stringToParse == "aika"):
        return ((TokenValues.WHILE, stringToParse, linenr))

    if (stringToParse == "lig"):
        return ((TokenValues.EQUAL, stringToParse, linenr))
    if (stringToParse == "unterschiedlich"):
        return ((TokenValues.NOTEQUAL, stringToParse, linenr))
    if (stringToParse == ">="):
        return ((TokenValues.GE, stringToParse, linenr))
    if (stringToParse == "<="):
        return ((TokenValues.SE, stringToParse, linenr))
    if (stringToParse == ">"):
        return ((TokenValues.GREATER, stringToParse, linenr))
    if (stringToParse == "<"):
        return ((TokenValues.SMALLER, stringToParse, linenr))

    if (stringToParse == "fin"):
        return ((TokenValues.SEMICOLON, stringToParse, linenr))
    if (stringToParse == "haakje_begin"):
        return ((TokenValues.LPAREN, stringToParse, linenr))
    if (stringToParse == "haakje_eind"):
        return ((TokenValues.RPAREN, stringToParse, linenr))
    if (stringToParse == "fa_inizio"):
        return ((TokenValues.LBRACE, stringToParse, linenr))
    if (stringToParse == "fa_fine"):
        return ((TokenValues.RBRACE, stringToParse, linenr))
    if (stringToParse == "taispeain"):
        return ((TokenValues.PRINT, stringToParse, linenr))
    if (stringToParse == "#"):
        return ((TokenValues.PRINT_END, stringToParse, linenr))
    if (re.fullmatch("^[@][a-zA-Z0-9_]*", stringToParse)):
        return ((TokenValues.VAR, stringToParse, linenr))

    else:
        return ((TokenValues.ERROR, stringToParse, linenr))

# fileToWordlist :: str -> List[str]
def fileToWordlist(string_file : str) -> List[str]:
    """Creates wordlist through string, removes unnecessary chars such as \n \t \r and spaces and returns list with words"""
    wordlist = createWordlist(string_file)
    # filter empty characters
    wordlist = list(filter((lambda x: x != ''), wordlist))
    return wordlist

# createWordlist :: str -> List[str]
def createWordlist(string_file : str) -> List[str]:
    """gets string and adds word to list of strings, delimiter is ' ', '\t', '\n', '\r' """
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

# foldl :: (A, B, C) -> B -> List[A] -> List[C]
def foldl(f: Callable[[A, B], C], base : B, list : List[A]) -> List[C]:
    """Creates new list according to the input function"""
    if(len(list) == 0):
        return base
    head, *tail = list
    return (f(head, foldl(f, base, tail)))

A = TypeVar('A')
B = TypeVar('B')

# wordlistToTokens (A -> B -> Token) -> List[str] -> int -> List[Token]
def wordlistToTokens(f : Callable [[A, B], Token], wordlist : List[str], linenr : int) -> (List[Token]):
    """Creates List[Tuple] for every word in the list and corresponding the linenumber and foldl this to return the corresponding Token"""
    line_list = [linenr] * len(wordlist)
    string_and_line = list((zip(wordlist,line_list)))
    tokenlist = foldl(f,[], (string_and_line))
    return tokenlist

# read_rec :: io.TextIOWrapper -> List[str]
def read_rec(f : io.TextIOWrapper) -> List[str]:
    """Read per line the content and add to list. The result is a list with elements per line of the file.
    It ignores the comments"""
    read = (f.readline())
    if (read == ""):
        return [read]
    # check if line is comment
    if(read[0] == "$"):
        read = "" # add an empty list, so the linenumbers will stay correct
    return [read] + read_rec(f)

# readFromFile :: str -> -> List[str] | None
def readFromFile(filename : str) -> Union[List[str], None]:
    """open file and read file per row recursively to fill the list per line.
    Return the list with the file content or none if the file could not be opened"""
    if(os.access(filename, os.R_OK)):
        f = open(filename, "r")
        lines = read_rec(f)
        f.close()
        return lines
    return None

# function_wordToTuple :: Tuple[str,int] -> List[Token] -> List[Token]
def function_TupleToToken(x : Tuple[str,int], tail : List[Token]) -> List[Token]:
    """Unpack tuple and return Token"""
    return [Token(returnTupleFromString(x[0], x[1]))] + tail

# lex_func :: str -> int -> List[Token]
def lex_func(file_line : str, linenr : int) -> List[Token]:
    """Receives a string that contains a line of code. Returns the corresponding Tokens of this line"""
    wordlist = fileToWordlist(file_line) # create wordlist from string
    tokenlist = wordlistToTokens(function_TupleToToken, wordlist, linenr)
    return tokenlist

# lex_rec :: (str -> int -> List[Token]) -> List[str] -> List[Token]
def lex_rec(f : Callable[[str,int], List[Token]], fileContainer : List[str]) -> List[Token]:
    """Per element in the list it retrieves the corresponding list of Tokens
    Every element in the list stands for a file-line"""
    if(len(fileContainer) <= 0):
        return []
    return lex_rec(f, fileContainer[:-1]) + f(fileContainer[-1], len(fileContainer))

# lexer -> str -> Tuple[List[Token], Error] | Tuple[None, Error]
def lexer(filename : str) -> Union[Tuple[List[Token], Error], Tuple[None, Error]]:
    """Reads from file the content. If None is returned, show error
    else retrieve the tokens matching to the inputted lines. If a Token could not be parsed, create error and return result"""
    fileContainer = readFromFile(filename)
    if(fileContainer != None):
        tokenlist = lex_rec(lex_func, fileContainer)
        errorlist = list(filter(lambda x: x.instance == TokenValues.ERROR, tokenlist))
        error = Error(Errornr.NO_ERROR)
        if (len(errorlist) > 0):
            error = (Error(Errornr.SYNTAX_ERROR, "On line " + str(errorlist[0].linenr) + ", cannot define " + " \"" + errorlist[0].type + "\" " + " "))
        return tokenlist, error
    return None, Error(Errornr.FileNotFoundError, "Cannot open " + filename)

