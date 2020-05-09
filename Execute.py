from typing import Tuple, List, Callable, Union, TypeVar
from Parser import Node, operator_node, value_node
from Enums import Error, Errornr, TokenValues

class ProgramActions():
    def __init__(self):
        self.variables = {}
        self.enum_dict = {}
        self.devide = smart_devide(lambda x, y : x/y)
        self.enum_dict[TokenValues.PLUS.value] = lambda a, b : a + b
        self.enum_dict[TokenValues.MIN.value] = lambda a, b: a - b
        self.enum_dict[TokenValues.MULTIPLY.value] = lambda a, b: a * b
        self.enum_dict[TokenValues.DIVIDED_BY.value] = lambda a, b: self.devide(a,b)
        self.enum_dict[TokenValues.ASSIGN.value] = lambda d, key, value: d.update({key:value})
        self.enum_dict[TokenValues.EQUAL.value] = lambda a, b : a == b
        self.enum_dict[TokenValues.NOTEQUAL.value] = lambda a, b: a != b
        self.enum_dict[TokenValues.GE.value] = lambda a, b: a >= b
        self.enum_dict[TokenValues.SE.value] = lambda a, b: a <= b
        self.enum_dict[TokenValues.GREATER.value] = lambda a, b: a > b
        self.enum_dict[TokenValues.SMALLER.value] = lambda a, b: a < b
        self.enum_dict[TokenValues.IF.value] = lambda enum, a, b: iffunc(enum, a, b)
        self.enum_dict[TokenValues.WHILE.value] = lambda enum, a, b: whilefunc(enum,a,b)
        self.enum_dict[TokenValues.VAR.value] = lambda enum, a, b: enum.variables[a]
        self.enum_dict[TokenValues.PRINT.value] = lambda enum, a, b : print_func(enum, b)

def print_func(enum, b : List[Node]) -> None:
    if(b != None):
        enum_list = [enum] * len(b)
        # cast to list, so the map will be executed and not optimized and removed
        list(map(lambda x, y: print(_loopNode(x, y)[0]), enum_list, b))


def iffunc (enum : ProgramActions, a : bool, b : List[Node]) -> Error:
    error = Error()
    if(a):
        result, error = AST_to_actions(enum,b)
    return error

def whilefunc(enum : ProgramActions, a : List[Node], b : List[Node]) -> Error:
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

A = TypeVar('A')
B = TypeVar('B')
def smart_devide(f : Callable) -> Union[Callable[[A, B],A|B], float, int, Error]:
    def inner(a, b):
        if(b == 0):
            return Error(Errornr.ZeroDivisionError, "cannot divide "+ str(a) + " with " + str(b))
        return f(a,b)
    return inner

def execute(enum : ProgramActions, key : TokenValues, arg : Tuple) -> Union[float, Error]:
    if(key == TokenValues.ASSIGN):
        return enum.enum_dict[key.value](*(enum.variables, *(arg)))
    if (key == TokenValues.IF or key == TokenValues.WHILE or key == TokenValues.VAR or key == TokenValues.PRINT):
        return enum.enum_dict[key.value](*(enum, *(arg)))
    return enum.enum_dict[key.value](*arg)

def _loopNode(enum : ProgramActions, node : Node) -> Tuple[Union[None,float,str], Error]:

    if(isinstance(node, value_node)):
        if (node.type == TokenValues.NUMBER):
            return float(node.value), Error()
        if (node.type == TokenValues.VAR):
            if(node.value in enum.variables):
                return enum.variables[node.value], Error()
            else:
                return (None, Error(Errornr.NameError, "On line " + str(node.linenr) + ", name \"" + node.value + "\" is not defined"))
        if (node.type == TokenValues.VAR_ASSIGN):
            return node.value, Error()

    if(isinstance(node, operator_node)):
        # use different call for whileloop
        if (node.operator == TokenValues.WHILE):
            error = execute(enum, node.operator, ([node.lhs], node.rhs))
            return None, error

        if (node.lhs == None or node.rhs == None):
            return None, Error(Errornr.SYNTAX_ERROR, "on line: " + str(node.linenr))
        left, error = _loopNode(enum, node.lhs)
        if(error.nr != Errornr.NO_ERROR):
            return None, error

        if ((not isinstance(node.rhs, list))):
            right, error = _loopNode(enum, node.rhs)
            if (error.nr != Errornr.NO_ERROR):
                return None, error

        else:
            right = node.rhs
        result = execute(enum, node.operator, (left, right))
        if(isinstance(result, Error)):
            return None, result
        return result, Error()
    # if empty node occurs, no big deal
    return None,Error()

def AST_to_actions(enum : ProgramActions, nodes : List[Node]) -> Tuple[Union[None,float], Error]:
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