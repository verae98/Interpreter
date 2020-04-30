from typing import Tuple

class enum():
    def __init__(self):
        self.variables = {}
        self.enum_dict = {}
        self.enum_dict["PLUS"] = lambda a, b : a + b
        self.enum_dict["MIN"] = lambda a, b: a - b
        self.enum_dict["MULTIPLY"] = lambda a, b: a * b
        self.enum_dict["DEVIDED_BY"] = lambda a, b: a / b
        self.enum_dict["ASSIGN"] = lambda d, key, value: d.update({key:value})
        self.enum_dict["EQUAL"] = lambda a, b : a == b
        self.enum_dict["NOTEQUAL"] = lambda a, b: a != b
        self.enum_dict["GE"] = lambda a, b: a >= b
        self.enum_dict["SE"] = lambda a, b: a <= b
        self.enum_dict["GREATER"] = lambda a, b: a > b
        self.enum_dict["SMALLER"] = lambda a, b: a < b
        self.enum_dict["IF"] = lambda a, b: self.iffunc(a, b)
        self.enum_dict["WHILE"] = lambda a, b: self.whilefunc(a, b)
        self.enum_dict["VAR"] = lambda a, b: self.getvariable(a)

    def whilefunc(self, a, b):
        self.AST_to_actions(b)

    def getvariable(self, a):
        return self.variables[a]

    def iffunc(self, a, b):
        if(a):
            self.AST_to_actions(b)

    def execute(self, key : str, arg : Tuple):
        if(key == "ASSIGN"):
            return self.enum_dict[key](*(self.variables, *(arg)))
        return self.enum_dict[key](*arg)

    def _loopNode(self, node):

        if(node.operator == "NUMBER"):
            return float(node.value)
        if(node.operator == "VAR"):
            return self.variables[node.value]
        if(node.operator == "WHILE"):
            if (node.lhs != None):
                left = self._loopNode(node.lhs)
                while (left):
                    self.execute(str(node.operator), (left, node.rhs))
                    left = self._loopNode(node.lhs)

            return

        if(node.lhs == None and node.rhs == None):
            return node.value
        left = None
        right = None

        if(node.lhs != None):
            left = self._loopNode(node.lhs)
        if(node.rhs != None and (not isinstance(node.rhs, list))):
            right = self._loopNode(node.rhs)
        else:
            right = node.rhs
        return self.execute(str(node.operator), (left, right))

    def AST_to_actions(self, nodes):
        if(len(nodes) == 0):
            return
        self.AST_to_actions(nodes[0:-1])
        print(self._loopNode(nodes[-1]))