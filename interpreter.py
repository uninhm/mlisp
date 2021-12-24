from sys import stderr

from parser import Scope, Keyword, IdentifierRef, Literal, FunctionDefinition, FunctionCall, If, ConstantDefinition
# from lexer import Token, TokenType

class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body
    
    def __str__(self) -> str:
        return "Function"

    def __repr__(self) -> str:
        return self.__str__()

class Interpreter:
    def run(self, expr, scope):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, IdentifierRef):
            if expr.name in scope:
                return scope[expr.name]
            else:
                raise Exception(f"{expr.pos}: Undefined identifier: {expr.name}")
        elif isinstance(expr, FunctionDefinition):
            if expr.name in scope:
                print(f'Warning: redefining `{expr.name}`', file=stderr)
            func = Function(expr.args, expr.body)
            scope.add(expr.name, func)
            return func
        elif isinstance(expr, ConstantDefinition):
            if expr.name in scope:
                print(f'Warning: redefining `{expr.name}`', file=stderr)
            val = self.run(expr.value, scope)
            scope.add(expr.name, val)
            return val
        elif isinstance(expr, If):
            if self.run(expr.condition, scope):
                return self.run(expr.body, scope)
            else:
                return self.run(expr.else_body, scope)
        elif isinstance(expr, Keyword):
            return expr.name
        elif isinstance(expr, FunctionCall) and not isinstance(expr.op, Keyword):
            op = self.run(expr.op, scope)
            if not isinstance(op, Function):
                raise Exception(f'{expr.pos}: `{op}` is not callable')
            if len(expr.args) != len(op.args):
                raise Exception(f'{expr.pos}: `{op}` expected {len(op.args)} arguments, got {len(expr.args)}')
            subscope = Scope(scope)
            for i in range(len(expr.args)):
                subscope.add(op.args[i], self.run(expr.args[i], scope))
            for o in op.body[:-1]:
                self.run(o, subscope)
            return self.run(op.body[-1], subscope)

        assert isinstance(expr.op, Keyword)

        op = expr.op.name
        if op == '+':
            s = 0
            for arg in expr.args:
                s += self.run(arg, scope)
            return s
        elif op == '-':
            s = self.run(expr.args[0], scope)
            for arg in expr.args[1:]:
                s -= self.run(arg, scope)
            return s
        elif op == '*':
            p = 1
            for arg in expr.args:
                p *= self.run(arg, scope)
            return p
        elif op == '/':
            d = self.run(expr.args[0], scope)
            for arg in expr.args[1:]:
                d /= self.run(arg, scope)
            return d
        elif op == 'div':
            d = self.run(expr.args[0], scope)
            for arg in expr.args[1:]:
                d //= self.run(arg, scope)
            return d
        elif op == 'mod':
            if len(expr.args) != 2:
                raise Exception(f'{expr.pos}: `mod` takes exactly two arguments')
            return self.run(expr.args[0], scope) % self.run(expr.args[1], scope)
        elif op == '=':
            if len(expr.args) != 2:
                raise Exception(f'{expr.pos}: = takes exactly two arguments')
            return self.run(expr.args[0], scope) == self.run(expr.args[1], scope)
        elif op == '<':
            if len(expr.args) != 2:
                raise Exception(f'{expr.pos}: < takes exactly two arguments')
            return self.run(expr.args[0], scope) < self.run(expr.args[1], scope)
        elif op == '>':
            if len(expr.args) != 2:
                raise Exception(f'{expr.pos}: > takes exactly two arguments')
            return self.run(expr.args[0], scope) > self.run(expr.args[1], scope)
        elif op == 'or':
            for arg in expr.args:
                if self.run(arg, scope):
                    return True
            return False
        elif op == 'and':
            for arg in expr.args:
                if not self.run(arg, scope):
                    return False
            return True
        elif op == 'not':
            if len(expr.args) != 1:
                raise Exception(f'{expr.pos}: `not` takes exactly one argument')
            return not self.run(expr.args[0], scope)
        # TODO: Replace print and input with functions
        # in the stdlib, using the eventual file managing
        elif op == 'print':
            print(*(self.run(arg, scope) for arg in expr.args))
            return None
        elif op == 'input':
            if len(expr.args) > 1:
                raise Exception(f'{expr.pos}: `input` takes at most one argument')
            if len(expr.args) == 0:
                return input()
            else:
                return input(self.run(expr.args[0], scope))
        elif op == 'len':
            if len(expr.args) != 1:
                raise Exception(f'{expr.pos}: `len` takes exactly one argument')
            return len(self.run(expr.args[0], scope))
        elif op == 'idx':
            # TODO: Find a better way to do this
            # probably when the language have types
            if len(expr.args) != 2:
                raise Exception(f'{expr.pos}: `idx` takes exactly two arguments')
            a = self.run(expr.args[0], scope)
            if isinstance(a, str):
                return ord(a[self.run(expr.args[1], scope)])
            else:
                return a[self.run(expr.args[1], scope)]
