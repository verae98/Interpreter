from Lexer import lexer, Token
from Parser import Node
from Execute import enum
from typing import List

import time

def processTokens(tokens: List[Token]) -> [Node]:
    if(len(tokens) == 0):
        return [Node()]

    nodes = processTokens(tokens[0:-1])
    currentToken = tokens[-1]
    current_node = nodes[-1]
    new_node = Node(currentToken.type)
    if(currentToken.instance == "PLUS"):
        if(len(nodes) <= 1):
            current_node.operator = currentToken.instance
            current_node.value = currentToken.type
        else:
            new_node.operator = currentToken.instance
            new_node.lhs = current_node
            nodes.append(new_node)

    else:
        if(current_node.lhs == None):
            nodes[-1].lhs = new_node
        elif (nodes[-1].rhs == None):
            nodes[-1].rhs = new_node
    return nodes


if __name__ == '__main__':
    lexer_list = lexer("test.txt")
    print(lexer_list)
    tree = (processTokens(lexer_list))
    print("--")
    print(tree)

    enum.AST_to_actions(enum(), tree)
