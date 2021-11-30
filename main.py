from lexer import Lexer
from parser import Parser, Scope
from interpreter import Interpreter

from sys import argv, setrecursionlimit

def main():
  lexer = Lexer()
  parser = Parser()
  interpreter = Interpreter()
  tokens = []
  while (line := input()) != 'exit':
    tokens += lexer.make_tokens(line)
    op = parser.parse(tokens)
    if op == 'WFMT':
      continue
    if op is not None:
      print(interpreter.run(op))
    tokens = []

if __name__ == '__main__':
  setrecursionlimit(1000000000)
  if len(argv) > 1:
    with open(argv[1]) as f:
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
      for op in ('div', 'mod', 'def', 'if', 'cond', 'or', 'and', 'not'):
        global_scope.add(op, op)
      
      for instruction in parser.parse(lexer.make_tokens(f.read())):
        print(interpreter.run(instruction, global_scope))
  else:
    main()