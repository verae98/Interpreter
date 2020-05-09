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
        self.enum_dict[TokenValues.IF.value] = lambda enum, a, b: if_func(enum, a, b)
        self.enum_dict[TokenValues.WHILE.value] = lambda enum, a, b: while_func(enum,a,b)
        self.enum_dict[TokenValues.VAR.value] = lambda enum, a, b: enum.variables[a]
        self.enum_dict[TokenValues.PRINT.value] = lambda enum, a, b : print_func(enum, b)

#print_func :: ProgramActions -> List[Node] -> None
def print_func(enum : ProgramActions, b : List[Node]) -> None:
    '''Print the values of the nodes b
    for every node, print the result of the _loopNode function'''
    if(b != None):
        enum_list = [enum] * len(b)
        # cast to list, so the map will be executed and not optimized and removed
        list(map(lambda x, y: print(_loopNode(x, y)[0]), enum_list, b))

# if_func :: ProgramActions -> Bool -> List[Node] -> Error
def if_func (enum : ProgramActions, a : bool, b : List[Node]) -> Error:
    '''if the condition is true, execute the nodes in list b
    Return the first error'''
    error = []
    if(a):
        # execute the codeblock in the ifstatement
        result, _error = AST_to_actions(enum,b)
        error.append(_error)
    #check if an error has occured. If so, return the error. Else, return NO-Error
    errors = list(filter(lambda x: x.nr != Errornr.NO_ERROR, error))
    if(len(errors)>0):
        return errors[0]
    return Error()

# while_func :: ProgramActions -> List[Node] -> List[Node] -> Error
def while_func(enum : ProgramActions, while_condition : List[Node], codeBlock : List[Node]) -> Error:
    '''check if the condition is true, then execute the codeblock
    check the condition_nodes every time, since the condition can be updated due to the codeblock'''
    condition, error = AST_to_actions(enum,while_condition)
    if(error.nr != Errornr.NO_ERROR):
        return error
    while(condition):
        #execute the code in the codeblok of the whileloop
        result, error = AST_to_actions(enum,codeBlock)
        if (error.nr != Errornr.NO_ERROR):
            return error
        # check if the condition is still true
        condition, error = AST_to_actions(enum, while_condition)
        # check for errors
        if (error.nr != Errornr.NO_ERROR):
            return error
    return Error()


A = TypeVar('A')
B = TypeVar('B')
# smart_devide :: Callable[[A|B, A|B], A|B] -> Callable[[A, B], A|B]
# inner : A -> B -> A | B | Error
def smart_devide(f : Callable[[A, B],Union[A,B]]) -> Callable[ [A,B],Union[A,B] ]:
    '''Define the inner function and return the function'''
    def inner(a : A, b : B) -> Union[A, B, Error]:
        '''Check if b is not 0: if not, return the devision, else return a zeroDivisionError'''
        if(b == 0):
            return Error(Errornr.ZeroDivisionError, "cannot divide "+ str(a) + " with " + str(b))
        return f(a,b)
    return inner

A = TypeVar('A')
B = TypeVar('B')
# execute :: ProgramActions -> TokenValues -> Tuple[A,B] -> float|Error
def execute(enum : ProgramActions, key : TokenValues, arg : Tuple[A,B]) -> Union[float, Error]:
    '''Call the correct dictionary corresponding with the TokenValue, return result or error'''
    if(key == TokenValues.ASSIGN):
        return enum.enum_dict[key.value](*(enum.variables, *(arg)))
    if (key == TokenValues.IF or key == TokenValues.WHILE or key == TokenValues.VAR or key == TokenValues.PRINT):
        return enum.enum_dict[key.value](*(enum, *(arg)))
    return enum.enum_dict[key.value](*arg)

# _loopNode :: ProgramActions -> Node -> Tuple[Union[None,float,str], Error]
def _loopNode(enum : ProgramActions, node : Node) -> Tuple[Union[None,float,str], Error]:
    '''Loop through the node. If an error occurs, return the error'''
    if(isinstance(node, value_node)):
        if (node.type == TokenValues.NUMBER):
            return float(node.value), Error()
        if (node.type == TokenValues.VAR):
            # check if the value is in the dictionary
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
        # Check if the nodes are filled, this is obligated
        if (node.lhs == None or node.rhs == None):
            return None, Error(Errornr.SYNTAX_ERROR, "on line: " + str(node.linenr))
        # get lhs
        left, error = _loopNode(enum, node.lhs)
        if(error.nr != Errornr.NO_ERROR):
            return None, error
        #check if node is a list (for the if-statement function)
        if ((not isinstance(node.rhs, list))):
            right, error = _loopNode(enum, node.rhs)
            if (error.nr != Errornr.NO_ERROR):
                return None, error

        else:
            right = node.rhs

        result = execute(enum, node.operator, (left, right))
        # check if the result is an error
        if(isinstance(result, Error)):
            return None, result
        # return result and No-error
        return result, Error()
    # if empty node occurs, no big deal
    return None,Error()

# AST_to_actions :: ProgramActions -> List[Node] -> Tuple[Union[None,float], Error]
def AST_to_actions(enum : ProgramActions, nodes : List[Node]) -> Tuple[Union[None,float], Error]:
    '''Loop throught the list of nodes and give the AST to the _loopNodeFunction. If an error occurs, stop the loop and return None and the error'''
    if(len(nodes) == 0):
        return None, Error()
    result, error_ast = AST_to_actions(enum, nodes[0:-1])
    #check for errors
    if (error_ast.nr != Errornr.NO_ERROR):
        return None, error_ast
    # unpack the AST
    result, error = _loopNode(enum, nodes[-1])
    if (error.nr != Errornr.NO_ERROR):
        return None, error
    #useful for whileloop
    return result, error