from sys import argv

from lexer import Lexer
from parser import Parser
from compiler import Compiler

compiler = Compiler()

def main_file(file_name):
    lexer = Lexer()
    parser = Parser()
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

def usage():
    print("Usage: python3 main.py [OPTIONS] <file>")
    print("OPTIONS:")
    print("  -nasm       Compile to NASM assembly instead of FASM")
    print("  -debug      Add debug comments to the assembly")
    print("  -o <file>   Compile to <file> instead of `out.asm`")

def main():
    i = 1
    while i < len(argv):
        if argv[i] == "-nasm":
            compiler.nasm = True
            i += 1
        elif argv[i] == "-debug":
            compiler.debug = True
            i += 1
        elif argv[i] == "-o":
            i += 1
            compiler.output_filename = argv[i]
            i += 1
        else:
            main_file(argv[i])
            break
    else:
        usage()
        exit(1)

if __name__ == '__main__':
    main()
