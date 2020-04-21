from typing import List, Tuple
from Lexer import Token

class Node():

    def __init__(self, value = None, lhs = None, operator = None, rhs = None):
        self.value = value
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return ("(value: " + (" None " if self.value is None else self.value) + " lhs: " + (" None " if self.lhs is None else self.lhs.__repr__())
                + " operator: " + (" None " if self.operator is None else self.operator) + " rhs: " + (" None " if self.rhs is None else self.rhs.__repr__()) + ")\n")


    def __repr__(self):
        return self.__str__()

class operator_node():

    def __init__(self, lhs = None, operator = None, rhs = None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return (str(self.lhs) + " " + str(self.operator) + " " + str(self.rhs))

    def __repr__(self):
        return self.__str__()

class number_node():
    def __init__(self, token : Token):
        self.token = token.instance
        self.value = token.type
    def __str__(self):
        return (str(self.token) + " " + str(self.value) )

    def __repr__(self):
        return self.__str__()

class statement():
    def __init__(self , s):
        self.block = s

class tree():
    def __init__(self):
        self.root = operator_node()
