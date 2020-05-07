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

#returnTupleFromString :: srt -> int -> Tuple[str, str, int]
def new_returnTupleFromString(stringToParse : str, linenr : int) -> (Tuple[str, str, int]):
    """Checks string and returns corresponding tuple"""
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
    if (stringToParse == "taispeain"):
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
    if (stringToParse == "#"):
        return (("PRINT_END", stringToParse, linenr))
    if (re.fullmatch("^[a-zA-Z_][a-zA-Z0-9_]*", stringToParse)):
        return (("VAR", stringToParse, linenr))

    else:
        return (("ERROR", stringToParse, linenr))

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
        errorlist = list(filter(lambda x: x.instance == "ERROR", tokenlist))
        error = Error(Errornr.NO_ERROR)
        if (len(errorlist) > 0):
            error = (Error(Errornr.SYNTAX_ERROR, "On line " + str(errorlist[0].linenr) + ", cannot define " + " \"" + errorlist[0].type + "\" " + " "))
        return tokenlist, error
    return None, Error(Errornr.FileNotFoundError, "Cannot open " + filename)

