from typing import List, Tuple, Union, Callable
from Lexer import Token
from Enums import Error, Errornr, State
import copy

class Node():

    def __init__(self, value : str = None, type : str = None):
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return ("(value: " + (" None " if self.value is None else self.value) + " Type: " + (
        " None " if self.type is None else self.type) + ")\n")

    def __repr__(self) -> str:
        return self.__str__()

class operator_node(Node):

    def __init__(self, value : str = None , lhs : Node = None , operator : str = None, rhs : Node = None):
        Node.__init__(self, value, operator)
        self.value = value
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self) -> str:
        return ("(value: " + (" None " if self.value is None else self.value) + " lhs: " + (" None " if self.lhs is None else self.lhs.__repr__())
                + " operator: " + (" None " if self.operator is None else self.operator) + " rhs: " + (" None " if self.rhs is None else self.rhs.__repr__()) + ")\n")

    def __repr__(self) -> str:
        return self.__str__()

class value_node(Node):
    def __init__(self, value : str = None, type : str = None):
        Node.__init__(self, value, type)
        self.value = value
        self.type = type

    def __str__(self):
        return ("(value: " + (" None " if self.value is None else self.value) + " Type: " + (" None " if self.type is None else self.type) + ")\n" )

    def __repr__(self):
        return self.__str__()

class ProgramValues():
    def __init__(self, state = State.Idle, unprocessed = list(), error_list = list()):
        self.state = state
        self.unprocessedTokens = unprocessed
        self.error_list = error_list

    def __str__(self):
        return "ProgramValues ( State: "  + str(self.state) + ", Unprocessed " + str(self.unprocessedTokens) + ", Errorlist " + str(self.error_list) + " )"

    def __repr__(self):
        return self.__str__()

def findNode(node : Node) -> Union[Node,None]:
    if(isinstance(node, operator_node)):
        if (node.lhs == None and node.rhs == None):
            return node
        if(node.rhs == None):
            return node
        if (isinstance(node.rhs, value_node)):
            return node
        if (node.rhs != None):
            return findNode(node.rhs)
    return None


def processMath(currentToken1: Token, current_node1 : Node) -> (Node, [Error]):
    error = []
    currentToken = copy.copy(currentToken1)
    current_node = copy.copy(current_node1)
    if (currentToken.instance == "PLUS" or currentToken.instance == "MIN"):
        new_node = operator_node(currentToken.type, current_node, currentToken.instance)
        return new_node, error
    elif (currentToken.instance == "MULTIPLY" or currentToken.instance == "DEVIDED_BY"):
        # find the node that is not filled yet
        node_ = findNode(current_node)
        if(node_ != None):
            lhs = node_.rhs
            new_node = operator_node(currentToken.type, lhs, currentToken.instance)
            node_.rhs = new_node
        else:
            # if there are only values in the nodetree
            new_node = operator_node(currentToken.type, current_node, currentToken.instance)
            current_node = new_node

    else:
        new_node = value_node(currentToken.type, currentToken.instance)
        # check if list is empty
        if(current_node.value == None):
            current_node = new_node
        else:
            # get empty operator_node
            node_ = findNode(current_node)
            if(node_ != None):
                if(node_.lhs == None):
                    node_.lhs = new_node
                elif (node_.rhs == None):
                    node_.rhs = new_node
                else:
                    error.append(Error(Errornr.MATH_ERROR, "On line: " + str(currentToken.linenr) + ", too many numbers versus operators"))
            else:
                error.append(Error(Errornr.MATH_ERROR, "On line: " + str(currentToken.linenr) + ", cannot calculate " + currentToken.type))
                pass
    return current_node, error

def processComparison(tokens1: List[Token]) -> (Node, [Error]):
    error = []
    tokens = copy.copy(tokens1)
    # get first element that meets the condition
    func = lambda currentToken: currentToken.instance == "EQUAL" or currentToken.instance == "NOTEQUAL" or currentToken.instance == "GE" \
        or currentToken.instance == "SE" or currentToken.instance == "GREATER" or currentToken.instance == "SMALLER"
    index = _getFirst(list(map(func, tokens)))

    lhs, pv = processTokens(tokens[:index])
    if(len(pv.error_list) > 0):
        error.append(pv.error_list)
    if (pv.state == State.ERROR or len(lhs) > 1 ):
        error.append(Error(Errornr.SYNTAX_ERROR, "On line " + str(tokens[0].linenr) + " ^" + str(tokens[0].type) + " invalid syntax: too many arguments for comparison"))
    rhs, pv = processTokens(tokens[index + 1:])
    if ((pv.state == State.ERROR or len(rhs) > 1) and len(error) == 0):
        error.append(Error(Errornr.SYNTAX_ERROR, "On line " + str(tokens[0].linenr) + " ^" + str(tokens[index + 1].type) + " invalid syntax: too many arguments for comparison"))
    current_node = operator_node(tokens[index].type, lhs[0], tokens[index].instance, rhs[0])
    return current_node, error


def processIf_While(tokens1: List[Token]) -> Union[Tuple[Node, ProgramValues], Tuple[None, List[Error]] ]:
    error = []
    tokens = copy.copy(tokens1)
    index_parL = getIndexToken(lambda x: x.instance == "LPAREN", tokens)
    index_parR = getIndexToken(lambda x: x.instance == "RPAREN", tokens)
    index_bracL = getIndexToken(lambda x: x.instance == "LBRACE", tokens)
    print(index_parR)
    print(index_bracL)
    if(index_parL == -1 or index_parR == -1):
        error.append(Error(Errornr.SYNTAX_ERROR, "Syntax Error on line " + str(tokens[0].linenr)))
        return None, error

    if((index_bracL - index_parR) != 1):
        print("1111111111111111111111")
        error.append(Error(Errornr.SYNTAX_ERROR, "Syntax Error on line " + str(tokens[index_parR].linenr)))
        return None, error
    elif(index_bracL == -1):
        error.append(Error(Errornr.SYNTAX_ERROR, "Syntax Error on line " + str(tokens[index_parR].linenr)))
        return None, error

    new_node = operator_node(tokens[0].type, None, tokens[0].instance)
    compare_node, error = processComparison(tokens[index_parL+1:index_parR])
    node_list_rhs, pv1 = processTokens(tokens[index_bracL+1:-1])
    pv = copy.copy(pv1)
    pv.unprocessedTokens = []
    if(len(error) > 0):
        pv.error_list.append(error)
        pv.state = State.ERROR
    new_node.lhs = compare_node
    new_node.rhs = node_list_rhs
    return new_node, pv

def processAssign(tokens1: List[Token]) -> (Node, ProgramValues):
    error = []
    tokens = copy.copy(tokens1)
    index = getIndexToken(lambda x: x.instance == "ASSIGN", tokens)
    if(index != 1):
        error.append(Error(Errornr.SYNTAX_ERROR, "too many arguments for assignment"))
    lhs = value_node(tokens[0].type, "VAR_ASSIGN")
    rhs, pv1 = processTokens(tokens[index+1:])
    pv = copy.copy(pv1)
    pv.unprocessedTokens = []
    if (pv.state == State.ERROR):
        pv.error_list.append(Error(Errornr.SYNTAX_ERROR, "Cannot process rhs"))
    if(len(rhs) > 1):
        pv.error_list.append(Error(Errornr.SYNTAX_ERROR, "too many arguments for assignment"))
    current_node = operator_node(tokens[index].type, lhs, tokens[index].instance, rhs[0])
    return current_node, pv


def processVar(token : Token) -> Node:
    return value_node(token.type, token.instance)

def _getFirst(list_to_check : List[bool]) -> int:
    if(len(list_to_check) == 0):
        return -1
    index = _getFirst(list_to_check[:-1])
    if(list_to_check[-1] and index == -1):
        return len(list_to_check) -1
    return index

def getIndexToken(f : Callable[[Token], bool], tokens : List[Token]) -> [int] :
    int_list = list(map(f, tokens))
    # get first element that has the match, return index
    return _getFirst(int_list)

def amountOpenBraces(tokens: List[Token]) -> int:
    if(len(tokens) <= 0):
        return 0
    braces = amountOpenBraces(tokens[:-1])
    currentToken = tokens[-1]
    if(currentToken.instance == "LBRACE"):
        braces = braces + 1
    elif(currentToken.instance == "RBRACE"):
        braces = braces - 1
    return braces

def processTokens(tokens: List[Token]) -> ([Node], ProgramValues):
    nodes, pv1 = _processTokens(tokens)
    pv1.unprocessedTokens = []
    pv = copy.copy(pv1)
    pv.unprocessedTokens = []

    return nodes, pv

def _processTokens(tokens1: List[Token]) -> ([Node], ProgramValues):
    tokens = copy.copy(tokens1)
    if(len(tokens) == 0):
        return [], ProgramValues(unprocessed = []) # default values

    nodes, pv_old = _processTokens(tokens[0:-1])
    pv = copy.copy(pv_old)
    currentToken = tokens[-1]
    if(pv.state == State.ERROR):
        return nodes, pv
    if (pv.state == State.Math):
        # program rules, assignment before math
        if (currentToken.instance == "ASSIGN"):
            pv.state = State.ASSIGN
            # remove incorrect math equation
            nodes = nodes[:-1]
            pv.unprocessedTokens.append(currentToken)
        elif (currentToken.instance != "NUMBER" and currentToken.instance != "VAR" and currentToken.instance != "PLUS" and currentToken.instance != "MIN" and
                    currentToken.instance != "MULTIPLY" and currentToken.instance != "DEVIDED_BY"):
            # math state is over, remove processed tokens
            pv.unprocessedTokens = []
            pv.state = State.Idle
        else:
            pv.unprocessedTokens.append(currentToken)
            nodes[-1], error = processMath(currentToken, nodes[-1])
            if(len(error) > 0):
                pv.state = State.ERROR
                pv.error_list.append(error)
        return nodes, pv

    elif (pv.state == State.ASSIGN):
        if(currentToken.instance == "SEMICOLON"):
            pv.unprocessedTokens.append(currentToken)
            new_node, pv = processAssign(pv.unprocessedTokens)
            if (len(pv.error_list) > 0):
                pv.state = State.ERROR
                return nodes, pv
            pv.unprocessedTokens = []
            nodes.append(new_node)
            pv.state = State.Idle
        else:
            pv.unprocessedTokens.append(currentToken)
        return nodes, pv

    elif(pv.state == State.IF_WHILE):
        pv.unprocessedTokens.append(currentToken)
        if(currentToken.instance == "RBRACE"):
            amountBraces = amountOpenBraces(pv.unprocessedTokens)
            if (amountBraces == 0):
                new_node, pv1 = processIf_While(pv.unprocessedTokens)
                if(new_node == None):
                    pv.state = State.ERROR
                    pv.error_list.append(pv1)
                    return nodes, pv
                nodes.append(new_node)
                pv.unprocessedTokens = []
                pv.state = State.Idle
                nodes.append(Node())
            elif (amountBraces < 0):
                print("error braces not correct")

        return nodes, pv


    elif(currentToken.instance == "PLUS" or currentToken.instance == "MIN" or
                 currentToken.instance == "MULTIPLY" or currentToken.instance == "DEVIDED_BY" or currentToken.instance == "NUMBER" or currentToken.instance == "VAR"):
        if(pv.state == State.Idle):
            pv.state = State.Math
            nodes.append(Node())
            #TODO: check meaning for this
            if (len(pv.unprocessedTokens) < 0):
                nodes[-1], error = processMath(pv.unprocessedTokens[0], nodes[-1])
                if (len(error) > 0):
                    state = State.ERROR
                    pv.error_list.append(error)
                    return nodes, pv

            nodes[-1], error = processMath(currentToken, nodes[-1])
            if (len(error) > 0):
                pv.state = State.ERROR
                pv.error_list.append(error)
                return nodes, pv


    elif (currentToken.instance == "ASSIGN"):
        if (pv.state == State.Idle):
            pv.state = State.ASSIGN


    elif(currentToken.instance == "IF"):
        pv.state = State.IF_WHILE

    elif (currentToken.instance == "WHILE"):
        pv.state = State.IF_WHILE

    pv.unprocessedTokens.append(currentToken)

    return nodes, pv



def parse(tokens: List[Token]) -> ([Node], ProgramValues):
    return processTokens(tokens)