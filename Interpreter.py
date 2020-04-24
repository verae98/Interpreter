from Lexer import lexer, Token
from Parser import Node
from Execute import enum
from typing import List, Union
from enum import Enum

import time

def findNode(node : Node) -> Union[Node,None]:
    if (node.lhs == None and node.rhs == None):
        return node
    if(node.rhs == None):
        return node
    if (node.rhs != None):
        return findNode(node.rhs)
    return None

def createBlock(tokens : List[Token]):
    nodes = processTokens(tokens[0:-1])


class State(Enum):
    Idle = 0
    Math = 1
    IF = 2
    IF_CONDITION = 3
    IF_BLOCK = 4
    BLOCK = 5
    ASSIGN = 6


def processMath(token: Token, current_node) -> Node:
    currentToken = token

    if (currentToken.instance == "PLUS" or currentToken.instance == "MIN"):
        new_node = Node(currentToken.type, current_node, currentToken.instance)
        current_node = new_node
    elif (currentToken.instance == "MULTIPLY" or currentToken.instance == "DEVIDED_BY"):
        node_ = findNode(current_node)
        new_node = Node(node_.value)
        node_.value = currentToken.type
        node_.operator = currentToken.instance
        node_.lhs = new_node

    else:
        new_node = Node(currentToken.type)
        # check if list is empty
        if(current_node.value == None):
            print("created node")
            current_node = new_node
        else:
            # get empty node
            node_ = findNode(current_node)
            if(node_.lhs == None):
                node_.lhs = new_node
            elif (node_.rhs == None):
                node_.rhs = new_node
    return current_node

def processComparison(token: Token, current_node) -> Node:

    currentToken = token

    if (currentToken.instance == "EQUAL" or currentToken.instance == "NOTEQUAL" or currentToken.instance == "GE"
        or currentToken.instance == "SE" or currentToken.instance == "GREATER" or currentToken.instance == "SMALLER"):
        new_node = Node(currentToken.type, current_node, currentToken.instance)
        current_node = new_node
    else:
        new_node = Node(currentToken.type)
        # check if list is empty
        if(current_node.value == None):
            current_node = new_node
        else:
            # get empty node
            node_ = findNode(current_node)
            if(node_.lhs == None):
                node_.lhs = new_node
            elif (node_.rhs == None):
                node_.rhs = new_node
    return current_node



def processIf(tokens: List[Token]) -> ([Node], State):
    if (len(tokens) == 0):
        return [Node()], State.Idle
    nodes, state = processIf(tokens[0:-1])
    currentToken = tokens[-1]
    current_node = nodes[-1]

    if (currentToken.instance == "IF"):
        new_node = Node(currentToken.type, None, currentToken.instance)
        nodes[-1] = new_node
        return nodes , State.IF_CONDITION
    if (state == State.IF_CONDITION):
        if (currentToken.instance == "LPAREN"):
            nodes.append(Node())
            return nodes, state
        if(currentToken.instance == "RPAREN"):
            state = State.BLOCK

            # set condition node to lhs of if node
            nodes[-2].lhs = nodes[-1]
            # current node is empty
            nodes[-1] = Node()

            return nodes, state
        else:
            nodes[-1] = processComparison(currentToken, current_node)
            return nodes, state

    if (state == State.IF_BLOCK):
        if (currentToken.instance == "LBRACE"):
            #nodes.append(Node())
            return nodes, state
        if (currentToken.instance == "RPAREN"):
            return nodes, state

    return nodes, state

def processTokens(tokens: List[Token]) -> ([Node], State, List[Token]):
    if(len(tokens) == 0):
        return [Node()], State.Idle, []

    nodes, state, unprocessedTokens = processTokens(tokens[0:-1])
    currentToken = tokens[-1]
    current_node = nodes[-1]

    if(currentToken.instance == "SEMICOLON"):
        state = State.Idle

        if (len(nodes) >= 2 and nodes[-2].operator == "ASSIGN" and nodes[-2].rhs == None):
            nodes[-2].rhs = nodes[-1]
            nodes[-1] = Node()
        else:
            nodes.append(Node())

    elif(state == State.Math):
        print("math")
        nodes[-1] = processMath(currentToken, current_node)
        return nodes, State.Math, unprocessedTokens

    elif(state == State.IF):
        unprocessedTokens.append(currentToken)
        if(currentToken.instance == "RBRACE"):
            new_node, status_if = processIf(unprocessedTokens)
            print ("-->")
            print(new_node)
            print("<--")
            nodes.append(new_node[0])
            unprocessedTokens = []
            state = State.Idle
            nodes.append(Node())

        return nodes, state, unprocessedTokens

    elif(currentToken.instance == "PLUS" or currentToken.instance == "MIN" or currentToken.instance == "MULTIPLY" or currentToken.instance == "DEVIDED_BY"):
        state = State.Math
        nodes[-1] = processMath(currentToken, current_node)

    elif (currentToken.instance == "ASSIGN"):
        new_node = Node(currentToken.type, current_node, currentToken.instance)
        nodes[-1] = new_node
        nodes.append(Node())

    elif(currentToken.instance == "IF"):
        unprocessedTokens.append(currentToken)
        state = State.IF

    else:
        new_node = Node(currentToken.type)
        # check if list is empty
        if(current_node.value == None):
            print("created node")
            nodes[-1] = new_node
        else:
            # get empty node
            node_ = findNode(current_node)
            if(node_.lhs == None):
                node_.lhs = new_node
            elif (node_.rhs == None):
                node_.rhs = new_node

    return nodes, state, unprocessedTokens


if __name__ == '__main__':

    lexer_list = lexer("test.txt")
    print(lexer_list)
    print ("\n")

    tree, state, _unprocessedTokens = processTokens(lexer_list)
    print("----------------")
    print(tree)


    exec = enum()
    print ("----------------")
    time.sleep(1)
    exec.AST_to_actions(tree)

    '''
    tree, state = processTokens(lexer_list)
    print("--")
    print(tree)
    time.sleep(1)
    exec = enum()
    exec.AST_to_actions(tree)
    print(exec.variables)'''
