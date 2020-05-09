from enum import Enum

class Errornr(Enum):
    NO_ERROR = "No Error"
    SYNTAX_ERROR = "Syntax Error"
    FileNotFoundError = "File Not Found Error"
    MATH_ERROR = "Math Error"
    NameError = "Name Error"
    ZeroDivisionError= "ZeroDivisionError"

class Error():
    def __init__(self, errornr : Errornr = Errornr.NO_ERROR, errormsg = ""):
        self.nr = errornr
        self.msg = errormsg

    def __str__(self):
        return (str(self.nr.value) + ": " + self.msg)

    def __repr__(self):
        return self.__str__()

class State(Enum):
    Idle = 0
    Math = 1
    ASSIGN = 2
    COMPARISON = 3
    ERROR = 4
    IF_WHILE = 5
    PRINT = 6

class TokenValues(Enum):
    PLUS = "PLUS"
    MIN = "MIN"
    MULTIPLY = "MULTIPLY"
    DIVIDED_BY = "DIVIDED_BY"
    NUMBER = "NUMBER"
    IF = "IF"
    ELSE = "ELSE"
    ASSIGN = "ASSIGN"
    WHILE = "WHILE"
    EQUAL = "EQUAL"
    NOTEQUAL = "NOTEQUAL"
    GE = "GE"
    SE = "SE"
    GREATER = "GREATER"
    SMALLER = "SMALLER"
    SEMICOLON = "SEMICOLON"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    PRINT = "PRINT"
    PRINT_END = "PRINT_END"
    VAR = "VAR"
    VAR_ASSIGN = "VAR_ASSIGN"
    ERROR = "ERROR"