from lexer import Token, TokenType

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.content = {}

    def add(self, name, value):
        self.content[name] = value

    def get(self, name):
        if name in self.content:
            return self.content[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None
    
    def __contains__(self, name):
        return name in self.content or (self.parent and name in self.parent)
    
    def __getitem__(self, name):
        return self.get(name)

class Expression:
    def __init__(self, op, args):
        self.op = op
        self.args = args
    
    def __str__(self):
        return 'Expression({op}, {args})'.format(
            op=self.op,
            args=self.args
        )
    
    def __repr__(self):
        return self.__str__()

class Function:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
    
    def __str__(self):
        return 'Function({name}, {args}, {body})'.format(
            name=self.name,
            args=self.args,
            body=self.body
        )
    
    def __repr__(self):
        return self.__str__()

class Parser:
    def step(self):
        self.idx += 1
        self.tok = self.tokens[self.idx] if self.idx < len(self.tokens) else None
    
    def def_expr(self):
        tok = self.tok
        self.step()
        if self.tok.check(TokenType.LEFT_PAREN): # it's a function
            self.step()
            if not self.tok.check(TokenType.IDENTIFIER):
                raise Exception('function name expected')

            name = self.tok.value
            self.step()
            args = []
            while self.tok.check(TokenType.IDENTIFIER):
                args.append(self.tok.value)
                self.step()

            if not self.tok.check(TokenType.RIGHT_PAREN):
                raise Exception('`)` expected in function definition')
            
            self.step()

            body = []
            while not self.tok.check(TokenType.RIGHT_PAREN):
                body.append(self.expr())
                
            if not self.tok.check(TokenType.RIGHT_PAREN):
                raise Exception('`)` expected after function definition')

            self.step()

            return Expression(tok, [name, args, body])
        else: # it's a constant
            if not self.tok.check(TokenType.IDENTIFIER):
                raise Exception('constant name expected')
            name = self.tok.value
            self.step()
            value = self.expr()
            if not self.tok.check(TokenType.RIGHT_PAREN):
                raise Exception('`)` expected after constant definition')
            self.step()
            return Expression(tok, [name, value])



    def if_expr(self):
        tok = self.tok
        self.step()
        p = self.expr()
        if_true = self.expr()
        if_false = self.expr()

        if not self.tok.check(TokenType.RIGHT_PAREN):
            raise Exception('`)` expected after if expression')
        
        self.step()

        return Expression(tok, [p, if_true, if_false])

    def cond_expr(self):
        pass
    
    def expr(self):
        if self.tok.check(TokenType.LEFT_PAREN):
            self.step()
            if self.tok.value == 'def':
                return self.def_expr()
            elif self.tok.value == 'if':
                return self.if_expr()
            elif self.tok.value == 'cond':
                return self.cond_expr()
            op = self.expr()
            args = []
            while not self.tok.check(TokenType.RIGHT_PAREN):
                args.append(self.expr())
            self.step()
            return Expression(op, args)
        else:
            tok = self.tok
            self.step()
            return tok
    
    def parse(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.step()

        while not self.tok.check(TokenType.EOF):
            yield self.expr()
