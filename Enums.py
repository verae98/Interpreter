from enum import Enum

class Errornr(Enum):
    NO_ERROR = "No Error"
    SYNTAX_ERROR = "Syntax Error"
    FileNotFoundError = "File Not Found Error"
    MATH_ERROR = "Math Error"

class Error():
    def __init__(self, errornr : Errornr, errormsg = ""):
        self.nr = errornr
        self.msg = errormsg

    def __str__(self):
        return (str(self.nr.value) + ": " + self.msg)

    def __repr__(self):
        return self.__str__()

class State(Enum):
    Idle = 0
    Math = 1
    IF_CONDITION = 3
    IF_BLOCK = 4
    ASSIGN = 6
    DONE = 7
    WHILE_CONDITION = 9
    WHILE_BLOCK = 10
    COMPARISON = 11
    ERROR = 12
    IF_WHILE = 13
    PRINT = 14