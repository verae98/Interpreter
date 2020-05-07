from Lexer import lexer, Token
from Parser import parse
from Execute import ProgramActions, AST_to_actions
from Enums import Errornr
from Parser import parse

import time

if __name__ == '__main__':
    lexer_list, errornr = lexer("test.txt")
    print(lexer_list)
    print( "------------------------")
    if(errornr.nr == Errornr.NO_ERROR):
        tree, pv = parse(lexer_list)
        if(len(pv.error_list) > 0):
            print(pv.error_list)
        elif(len(pv.unprocessedTokens) > 0):
            print("Error, the characters ", pv.unprocessedTokens, " have not been processed")
        else:
            print("TREE:")
            print(tree)

            time.sleep(1)

            exec = ProgramActions()
            result, error = AST_to_actions(exec, tree)
            if(error.nr != Errornr.NO_ERROR):
                print(error)
            else:
                print(exec.variables)

    else:
        print("Whoops: ")
        print(errornr)