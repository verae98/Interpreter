from Lexer import lexer, Token
from Parser import Node
from Execute import enum
from typing import List, Union

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

def processTokens(tokens: List[Token]) -> [Node]:
    if(len(tokens) == 0):
        return [Node()]

    nodes = processTokens(tokens[0:-1])
    currentToken = tokens[-1]
    current_node = nodes[-1]

    if(currentToken.instance == "PLUS" or currentToken.instance == "MIN"):
        new_node = Node(currentToken.type, current_node, currentToken.instance)
        nodes[-1] = new_node
    elif(currentToken.instance == "MULTIPLY" or currentToken.instance == "DEVIDED_BY"):
        node_ = findNode(current_node)
        new_node = Node(node_.value)
        node_.value = currentToken.type
        node_.operator = currentToken.instance
        node_.lhs = new_node
    elif (currentToken.instance == "SEMICOLON"):
        if(nodes[-2].operator == "ASSIGN" and nodes[-2].rhs == None):
            print("swich assign")
            nodes[-2].rhs = nodes[-1]
            print(nodes[-2])
            nodes[-1] = Node()
        else:
            nodes.append(Node())
    elif (currentToken.instance == "ASSIGN"):
        new_node = Node(currentToken.type, current_node, currentToken.instance)
        nodes[-1] = new_node
        nodes.append(Node())
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
    return nodes


if __name__ == '__main__':
    lexer_list = lexer("test.txt")
    print(lexer_list)
    tree = (processTokens(lexer_list))
    time.sleep(1)
    print("--")
    print(tree)
    exec = enum()
    exec.AST_to_actions(tree)
    print(exec.variables)
