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
    ASSIGN = 6
    DONE = 7


def processMath(tokens: [Token]) -> Node:
    if (len(tokens) == 0):
        return Node()
    nodes = processMath(tokens[0:-1])
    currentToken = tokens[-1]
    current_node = nodes

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



def processIf(tokens: List[Token], index : int) -> ([Node], State):
    if (index <= -1):
        return [Node()], State.Idle
    nodes, state = processIf(tokens, index-1)
    currentToken = tokens[index]
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
            state = State.IF_BLOCK
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
            nodes.append(Node())
            in_braces, state, unprocessed = processTokens(tokens[index+1:-1])
            nodes[0].rhs = in_braces
            state = State.DONE
            return nodes, state
        if (currentToken.instance == "RPAREN"):
            return nodes, state

    return nodes, state

def processAssign(tokens: List[Token], index : int) -> (Node, State):
    if (index <= -1):
        return Node(), State.Idle

    current_node, state = processAssign(tokens, index-1)
    currentToken = tokens[index]

    if (state == State.DONE):
        return current_node, state

    elif(state == State.ASSIGN):
        rhs, status, unprocessed = processTokens(tokens[index:])
        # returns list[Node] so get only first element
        current_node.rhs = rhs[0]
        state = State.DONE

    elif (currentToken.instance == "ASSIGN"):
        current_node = Node(currentToken.type, current_node, currentToken.instance)
        state = State.ASSIGN
    else:
        new_node = Node(currentToken.type)
        # check if list is empty
        if (current_node.value == None):
            current_node = new_node
        else:
            # get empty node
            time.sleep(1)
            node_ = findNode(current_node)
            if (node_.lhs == None):
                node_.lhs = new_node
            elif (node_.rhs == None):
                node_.rhs = new_node

    return current_node, state

def processTokens(tokens: List[Token]) -> ([Node], State, List[Token]):
    if(len(tokens) == 0):
        return [Node()], State.Idle, []

    nodes, state, unprocessedTokens = processTokens(tokens[0:-1])
    currentToken = tokens[-1]
    current_node = nodes[-1]

    if(currentToken.instance == "SEMICOLON"):
        if (state == State.Math):
            new_node = processMath(unprocessedTokens)
            nodes[-1] = (new_node)
            unprocessedTokens = []
            return nodes, State.Idle, unprocessedTokens

        if (state == State.ASSIGN):
            unprocessedTokens.append(currentToken)
            new_node, state_ = processAssign(unprocessedTokens, len(unprocessedTokens)-1)
            nodes.append(new_node)
            unprocessedTokens = []
            return nodes, State.Idle, unprocessedTokens
        if(state != State.Idle):
            unprocessedTokens.append(currentToken)
        else:
            state = State.Idle
            nodes.append(Node())


    elif(state == State.IF):
        unprocessedTokens.append(currentToken)
        if(currentToken.instance == "RBRACE"):
            new_node, status_if = processIf(unprocessedTokens, len(unprocessedTokens)-1)
            nodes.append(new_node[0])
            unprocessedTokens = []
            state = State.Idle
            nodes.append(Node())

        return nodes, state, unprocessedTokens

    elif(currentToken.instance == "PLUS" or currentToken.instance == "MIN" or currentToken.instance == "MULTIPLY" or currentToken.instance == "DEVIDED_BY"):
        if(state == State.Idle):
            state = State.Math
        unprocessedTokens.append(currentToken)

    elif (currentToken.instance == "ASSIGN"):
        unprocessedTokens.append(currentToken)
        if (state == State.Idle):
            state = State.ASSIGN

    elif(currentToken.instance == "IF"):
        unprocessedTokens.append(currentToken)
        state = State.IF

    else:
        unprocessedTokens.append(currentToken)

    return nodes, state, unprocessedTokens


if __name__ == '__main__':

    lexer_list = lexer("test.txt")
    print(lexer_list)
    #tree, state = processIf(lexer_list, len(lexer_list)-1)
    tree, state, unprocessed = processTokens(lexer_list)
    #tree, state = processAssign(lexer_list, len(lexer_list)-1)

    print("TREE:")
    print(tree)

    time.sleep(1)

    exec = enum()
    exec.AST_to_actions(tree)
    print(exec.variables)
