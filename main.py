from sys import argv, setrecursionlimit
import cmd

from lexer import Lexer, UnexpectedEOF
from parser import Parser
from interpreter import Interpreter, Scope

class CmdMain(cmd.Cmd):
    prompt = '>>> '
    tokens = []

    def default(self, line):
        if len(self.tokens) != 0:
            self.tokens.pop() # pop EOF
        self.tokens += lexer.make_tokens('<cmd>', line)
        try:
            for pres in parser.parse(self.tokens):
                if pres.error:
                    print(pres.error)
                    break
                op = pres.result
                if op is not None and \
                 (res := interpreter.run(op, global_scope)) is not None:
                    print(repr(res))
            self.tokens = []
            self.prompt = '>>> '
        except UnexpectedEOF:
            self.prompt = '... '

    def emptyline(self):
        pass

    def do_exit(self, _):
        return True

def main_file(file_name):
    with open(file_name, 'r') as f:
        for pres in parser.parse(lexer.make_tokens(file_name, f.read())):
            if pres.error:
                print(pres.error)
                break
            interpreter.run(pres.result, global_scope)

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

    if len(argv) > 1:
        main_file(argv[1])
    else:
        CmdMain().cmdloop()
