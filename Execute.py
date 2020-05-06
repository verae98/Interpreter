from typing import Tuple, List, Callable
from Parser import Node, operator_node, value_node

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
        self.enum_dict["IF"] = lambda enum, a, b: AST_to_actions(enum,b) if(a) else None
        self.enum_dict["WHILE"] = lambda enum, a, b: whilefunc(enum,a,b)
        self.enum_dict["VAR"] = lambda enum, a, b: enum.variables[a]
        self.enum_dict["PRINT"] = lambda a, b : print(b)

def whilefunc(enum : ProgramActions, a : List[Node], b : List[Node]):
    while(AST_to_actions(enum,a)):
        AST_to_actions(enum,b)

def smart_devide(f : Callable):
    def inner(a, b):
        if(b == 0):
            return
        return f(a,b)
    return inner

def execute(enum : ProgramActions, key : str, arg : Tuple):
    if(key == "ASSIGN"):
        return enum.enum_dict[key](*(enum.variables, *(arg)))
    if (key == "IF" or key == "WHILE" or key == "VAR"):
        return enum.enum_dict[key](*(enum, *(arg)))
    return enum.enum_dict[key](*arg)

def _loopNode(enum : ProgramActions, node : Node):

    if(isinstance(node, value_node)):
        if (node.type == "NUMBER"):
            return float(node.value)
        if (node.type == "VAR"):
            if(node.value in enum.variables):
                return enum.variables[node.value]
            else:
                print("UHOH DUNNO")
                return None
        if (node.type == "VAR_ASSIGN"):
            return node.value

    if(isinstance(node, operator_node)):
        # use different call for whileloop
        if (node.operator == "WHILE"):
            return execute(enum, str(node.operator), ([node.lhs], node.rhs))

        left = None
        right = None

        if (node.lhs != None):
            left = _loopNode(enum, node.lhs)
        if (node.rhs != None and (not isinstance(node.rhs, list))):
            right = _loopNode(enum, node.rhs)
        else:
            right = node.rhs
        return execute(enum, str(node.operator), (left, right))

def AST_to_actions(enum : ProgramActions, nodes : List[Node]):
    if(len(nodes) == 0):
        return
    AST_to_actions(enum, nodes[0:-1])
    #useful for whileloop
    return(_loopNode(enum, nodes[-1]))