from Lexer import lexer, Token
from Execute import ProgramActions, AST_to_actions
from Enums import Errornr
from Parser import parse

import time

if __name__ == '__main__':
    lexer_list, error = lexer("main.txt")
    if(error.nr == Errornr.NO_ERROR):
        tree, pv = parse(lexer_list)
        if(len(pv.error_list) > 0):
            print(pv.error_list[0])
        elif(len(pv.unprocessedTokens) > 0):
            print("Error, the characters on line", pv.unprocessedTokens[0].linenr, " could not be processed")
        else:
            time.sleep(1)

            exec = ProgramActions()
            result, error = AST_to_actions(exec, tree)
            if(error.nr != Errornr.NO_ERROR):
                print(error)

    else:
        print("Whoops: ")
        print(error)