from typing import Tuple

class enum():
    def __init__(self):
        self.variables = {}
        self.enum_dict = {}
        self.enum_dict["PLUS"] = lambda a, b : float(a) + float(b)
        self.enum_dict["MIN"] = lambda a, b: float(a) - float(b)
        self.enum_dict["MULTIPLY"] = lambda a, b: float(a) * float(b)
        self.enum_dict["DEVIDED_BY"] = lambda a, b: float(a) / float(b)
        self.enum_dict["ASSIGN"] = lambda d, key, value: d.update({key:value})
        self.enum_dict["EQUAL"] = lambda a, b : a == b

    def execute(self, key : str, arg : Tuple):
        if(key == "ASSIGN"):
            return self.enum_dict[key](*(self.variables, *(arg)))
        return self.enum_dict[key](*arg)

    def _loopNode(self, node):
        if(node.lhs == None and node.rhs == None):
            return node.value
        left = None
        right = None
        if(node.lhs != None):
            left = self._loopNode(node.lhs)
        if(node.rhs != None):
            right = self._loopNode(node.rhs)

        return self.execute(str(node.operator), (left, right))

    def AST_to_actions(self, nodes):
        if(len(nodes) == 0):
            return
        self.AST_to_actions(nodes[0:-1])
        self._loopNode(nodes[-1])