from sys import argv, setrecursionlimit
import cmd

from lexer import Lexer, UnexpectedEOF
from parser import Parser, Scope
from interpreter import Interpreter

class CmdMain(cmd.Cmd):
    prompt = '>>> '
    tokens = []

    def default(self, line):
        if len(self.tokens) != 0:
            self.tokens.pop() # pop EOF
        self.tokens += lexer.make_tokens(line)
        try:
            for op in parser.parse(self.tokens):
                if op is not None and \
                 (res := interpreter.run(op, global_scope)) is not None:
                    print(res)
            self.tokens = []
            self.prompt = '>>> '
        except UnexpectedEOF:
            self.prompt = '... '

    def emptyline(self):
        pass

    def do_exit(self, line):
        return True

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
        CmdMain().cmdloop()
