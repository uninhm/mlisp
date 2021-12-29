from sys import argv, setrecursionlimit

from lexer import Lexer, UnexpectedEOF
from parser import Parser
from compiler import Compiler

def main_file(file_name):
    with open(file_name, 'r') as f:
        exprs = []
        tokens = lexer.make_tokens(file_name, f.read())
        for pres in parser.parse(tokens):
            if pres.error:
                print(pres.error)
                exit(1)
            else:
                exprs.append(pres.result)
        else:
            compiler.compile_all(exprs)

if __name__ == '__main__':
    lexer = Lexer()
    parser = Parser()
    compiler = Compiler()
    if len(argv) > 1:
        main_file(argv[1])
    else:
        exit(1)
