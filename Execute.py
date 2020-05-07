from typing import Tuple, List, Callable, Union
from Parser import Node, operator_node, value_node
from Enums import Error, Errornr

class ProgramActions():
    def __init__(self):
        self.variables = {}
        self.enum_dict = {}
        self.devide = smart_devide(lambda x, y : x/y)
        self.enum_dict["PLUS"] = lambda a, b : a + b
        self.enum_dict["MIN"] = lambda a, b: a - b
        self.enum_dict["MULTIPLY"] = lambda a, b: a * b
        self.enum_dict["DEVIDED_BY"] = lambda a, b: self.devide(a,b)
        self.enum_dict["ASSIGN"] = lambda d, key, value: d.update({key:value})
        self.enum_dict["EQUAL"] = lambda a, b : a == b
        self.enum_dict["NOTEQUAL"] = lambda a, b: a != b
        self.enum_dict["GE"] = lambda a, b: a >= b
        self.enum_dict["SE"] = lambda a, b: a <= b
        self.enum_dict["GREATER"] = lambda a, b: a > b
        self.enum_dict["SMALLER"] = lambda a, b: a < b
        self.enum_dict["IF"] = lambda enum, a, b: iffunc(enum, a, b)
        self.enum_dict["WHILE"] = lambda enum, a, b: whilefunc(enum,a,b)
        self.enum_dict["VAR"] = lambda enum, a, b: enum.variables[a]
        self.enum_dict["PRINT"] = lambda enum, a, b : print_func(enum, b)

def print_func(enum, b : List[Node]):
    if(b != None):
        enum_list = [enum] * len(b)
        # cast to list, so the map will be executed and not optimized and removed
        list(map(lambda x, y: print(_loopNode(x, y)[0]), enum_list, b))


def iffunc (enum : ProgramActions, a : bool, b : List[Node]):
    error = Error()
    if(a):
        result, error = AST_to_actions(enum,b)
    return error

def whilefunc(enum : ProgramActions, a : List[Node], b : List[Node]):

    condition, error = AST_to_actions(enum,a)
    if(error.nr != Errornr.NO_ERROR):
        return error
    while(condition):
        result, error = AST_to_actions(enum,b)
        if (error.nr != Errornr.NO_ERROR):
            return error
        condition, error = AST_to_actions(enum, a)

        if (error.nr != Errornr.NO_ERROR):
            return error
    return Error()

def smart_devide(f : Callable):
    def inner(a, b):
        if(b == 0):
            return
        return f(a,b)
    return inner

def execute(enum : ProgramActions, key : str, arg : Tuple):
    if(key == "ASSIGN"):
        return enum.enum_dict[key](*(enum.variables, *(arg)))
    if (key == "IF" or key == "WHILE" or key == "VAR" or key == "PRINT"):
        return enum.enum_dict[key](*(enum, *(arg)))
    return enum.enum_dict[key](*arg)

def _loopNode(enum : ProgramActions, node : Node):

    if(isinstance(node, value_node)):
        if (node.type == "NUMBER"):
            return float(node.value), Error()
        if (node.type == "VAR"):
            if(node.value in enum.variables):
                return enum.variables[node.value], Error()
            else:
                return (None, Error(Errornr.NameError, "On line " + str(node.linenr) + ", name \"" + node.value + "\" is not defined"))
        if (node.type == "VAR_ASSIGN"):
            return node.value, Error()

    if(isinstance(node, operator_node)):
        # use different call for whileloop
        if (node.operator == "WHILE"):
            error = execute(enum, str(node.operator), ([node.lhs], node.rhs))
            return None, error

        left = None
        right = None

        if (node.lhs != None):
            left, error = _loopNode(enum, node.lhs)
            if(error.nr != Errornr.NO_ERROR):
                return None, error
        if (node.rhs != None and (not isinstance(node.rhs, list))):
            right, error = _loopNode(enum, node.rhs)
            if (error.nr != Errornr.NO_ERROR):
                return None, error
        else:
            right = node.rhs
        result = execute(enum, str(node.operator), (left, right))
        if(isinstance(result, Error)):
            return None, result
        return result, Error()
    # if empty node occurs
    return None,Error()

def AST_to_actions(enum : ProgramActions, nodes : List[Node]):
    if(len(nodes) == 0):
        return None, Error()
    result, error_ast = AST_to_actions(enum, nodes[0:-1])
    if (error_ast.nr != Errornr.NO_ERROR):
        return None, error_ast
    result, error = _loopNode(enum, nodes[-1])
    if (error.nr != Errornr.NO_ERROR):
        return None, error
    #useful for whileloop
    return result, error