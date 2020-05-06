from typing import Tuple, List, Callable
from Parser import Node, operator_node, value_node

class enum():
    def __init__(self):
        self.variables = {}
        self.enum_dict = {}
        self.devide = self.smart_devide(lambda x, y : x/y)
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
        self.enum_dict["IF"] = lambda a, b: self.AST_to_actions(b) if(a) else None
        self.enum_dict["WHILE"] = lambda a, b: self.whilefunc(a,b)
        self.enum_dict["VAR"] = lambda a, b: self.variables[a]
        self.enum_dict["PRINT"] = lambda a, b : print(b)

    def whilefunc(self, a : List[Node], b : List[Node]):
        while(self.AST_to_actions(a)):
            self.AST_to_actions(b)

    def smart_devide(self, f : Callable):
        def inner(a, b):
            if(b == 0):
                return
            return f(a,b)
        return inner

    def iffunc(self, a : bool, b : List[Node]):
        if(a):
            self.AST_to_actions(b)

    def execute(self, key : str, arg : Tuple):
        if(key == "ASSIGN"):
            return self.enum_dict[key](*(self.variables, *(arg)))
        return self.enum_dict[key](*arg)

    def _loopNode(self, node : Node):

        if(isinstance(node, value_node)):
            if (node.type == "NUMBER"):
                return float(node.value)
            if (node.type == "VAR"):
                return self.variables[node.value]
            if (node.type == "VAR_ASSIGN"):
                return node.value

        if(isinstance(node, operator_node)):
            # use different call for whileloop
            if (node.operator == "WHILE"):
                return self.execute(str(node.operator), ([node.lhs], node.rhs))

            left = None
            right = None

            if (node.lhs != None):
                left = self._loopNode(node.lhs)
            if (node.rhs != None and (not isinstance(node.rhs, list))):
                right = self._loopNode(node.rhs)
            else:
                right = node.rhs
            return self.execute(str(node.operator), (left, right))

    def AST_to_actions(self, nodes : List[Node]):
        if(len(nodes) == 0):
            return
        self.AST_to_actions(nodes[0:-1])
        #useful for whileloop
        return(self._loopNode(nodes[-1]))