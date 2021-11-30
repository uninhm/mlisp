from parser import Function, Expression, Scope
from lexer import Token, TokenType

class Interpreter:
    def run(self, expr, scope):
        if isinstance(expr, Token):
            if expr.type == TokenType.NUMBER:
                return expr.value
            elif expr.type == TokenType.IDENTIFIER:
                if expr.value in scope:
                    return scope[expr.value]
                else:
                    return None
            else:
                return expr

        op = self.run(expr.op, scope)
        if isinstance(op, Function):
            op = op.name
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
            d = self.run(expr.args[0])
            for arg in expr.args[1:]:
                d //= self.run(arg, scope)
            return d
        elif op == 'mod':
            if len(expr.args) != 2:
                raise Exception('`mod` takes exactly two arguments')
            return self.run(expr.args[0], scope) % self.run(expr.args[1], scope)
        elif op == '=':
            if len(expr.args) != 2:
                raise Exception('= takes exactly two arguments')
            return self.run(expr.args[0], scope) == self.run(expr.args[1], scope)
        elif op == '<':
            if len(expr.args) != 2:
                raise Exception('< takes exactly two arguments')
            return self.run(expr.args[0], scope) < self.run(expr.args[1], scope)
        elif op == '>':
            if len(expr.args) != 2:
                raise Exception('> takes exactly two arguments')
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
                raise Exception('`not` takes exactly one argument')
            return not self.run(expr.args[0], scope)
        elif op == 'def':
            scope.add(expr.args[0], Function(expr.args[0], expr.args[1], expr.args[2]))
            return expr.args[0]
        elif op == 'if':
            if self.run(expr.args[0], scope):
                return self.run(expr.args[1], scope)
            else:
                return self.run(expr.args[2], scope)
        else:
            if op in scope:
                if not isinstance(scope[op], Function):
                    raise Exception(f'`{op}` is not callable')
                if len(expr.args) != len(scope[op].args):
                    raise Exception(f'`{op}` expected {len(scope[op].args)} arguments, got {len(expr.args)}')
                subscope = Scope(scope)
                for i in range(len(expr.args)):
                    subscope.add(scope[op].args[i], self.run(expr.args[i], scope))
                op = scope[op].body
                return self.run(op, subscope)
            else:
                raise Exception(f'`{op}` does not exist so it cannot be called')