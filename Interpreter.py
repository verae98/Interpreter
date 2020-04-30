from Lexer import lexer, Token
from Parser import parse
from Execute import enum
from Enums import Errornr
from Parser import parse

import time

if __name__ == '__main__':

    lexer_list, errornr = lexer("test.txt")
    if(errornr.nr == Errornr.NO_ERROR):
        print(lexer_list)
        tree, state, unprocessed = parse(lexer_list)
        print("TREE:")
        print(tree)

        time.sleep(1)

        exec = enum()
        exec.AST_to_actions(tree)
        print(exec.variables)

    else:
        print("Error: ")
        print(errornr.nr)
        print(errornr.msg)