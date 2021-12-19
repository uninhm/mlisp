from sys import argv, setrecursionlimit

from lexer import Lexer, UnexpectedEOF
from parser import Parser, Scope
from interpreter import Interpreter

def main_interactive():
    tokens = []
    prompt = '>>> '
    while (line := input(prompt)) != 'exit':
        if len(tokens) != 0:
            tokens.pop() # pop EOF
        tokens += lexer.make_tokens(line)
        try:
            for op in parser.parse(tokens):
                if op is not None:
                    print(interpreter.run(op, global_scope))
            tokens = []
            prompt = '>>> '
        except UnexpectedEOF:
            prompt = '... '

def main_file(file_name):
    with open(file_name, 'r') as f:
        for instruction in parser.parse(lexer.make_tokens(f.read())):
            interpreter.run(instruction, global_scope)

if __name__ == '__main__':
    setrecursionlimit(1000000000)
    lexer = Lexer()
    parser = Parser()
    interpreter = Interpreter()
    global_scope = Scope()
    global_scope.content = {
        'true': True,
        'false': False,
    }
    for op in '+-=<>*/':
        global_scope.add(op, op)
    for op in ('print', 'div', 'mod', 'def', 'if', 'cond', 'or', 'and', 'not'):
        global_scope.add(op, op)

    if len(argv) > 1:
        main_file(argv[1])
    else:
        main_interactive()
