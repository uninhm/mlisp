from lexer import TokenType

class Expression:
    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()

class FunctionCall(Expression):
    def __init__(self, pos, op, args):
        super().__init__(pos)
        self.op = op
        self.args = args

    def __str__(self):
        return 'Expression({op}, {args})'.format(
            op=self.op,
            args=self.args
        )

class FunctionDefinition(Expression):
    def __init__(self, pos, name, args, body):
        super().__init__(pos)
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return 'Function({name}, {args}, {body})'.format(
            name=self.name,
            args=self.args,
            body=self.body
        )

class If(Expression):
    def __init__(self, pos, condition, body, else_body=None):
        super().__init__(pos)
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __str__(self):
        return 'If({condition}, {body}, {else_body})'.format(
            condition=self.condition,
            body=self.body,
            else_body=self.else_body
        )

class IdentifierRef(Expression):
    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name

    def __str__(self):
        return 'IdentifierRef({name})'.format(
            name=self.name
        )

class Keyword(Expression):
    def __init__(self, pos, name):
        super().__init__(pos)
        self.name = name

    def __str__(self):
        return 'Keyword({name})'.format(
            name=self.name
        )

class Literal(Expression):
    #TODO: Add type

    def __init__(self, pos, value):
        super().__init__(pos)
        self.value = value

    def __str__(self):
        return 'Literal({value})'.format(
            value=self.value
        )

class ConstantDefinition(Expression):
    def __init__(self, pos, name, value):
        super().__init__(pos)
        self.name = name
        self.value = value

    def __str__(self):
        return 'ConstantDefinition({name}, {value})'.format(
            name=self.name,
            value=self.value
        )

class LangError:
    def __init__(self, msg, pos):
        self.msg = msg
        self.pos = pos

    def __str__(self):
        return '{pos}: {errname}: {msg}'.format(
            pos=self.pos,
            errname=self.__class__.__name__,
            msg=self.msg
        )

    def __repr__(self):
        return self.__str__()

class ParsingError(LangError):
    pass

class Result:
    def __init__(self, result, error=None):
        self.result = result
        self.error = error

    def __str__(self):
        if self.error:
            return self.error.__str__()
        return self.result.__str__()

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        yield self.result
        yield self.error

class ParseResult(Result):
    pass

class Parser:
    def step(self):
        self.idx += 1
        self.tok = self.tokens[self.idx]

    def errorresult(self, msg):
        return ParseResult(None, ParsingError(msg, self.tok.pos))

    def def_expr(self) -> ParseResult:
        pos = self.tok.pos
        self.step()
        if self.tok.check(TokenType.LEFT_PAREN): # it's a function
            self.step()
            if not self.tok.check(TokenType.IDENTIFIER):
                return self.errorresult('function name expected')

            name = self.tok.value
            self.step()
            args = []
            while self.tok.check(TokenType.IDENTIFIER):
                args.append(self.tok.value)
                self.step()

            if not self.tok.check(TokenType.RIGHT_PAREN):
                return self.errorresult('`)` expected in function definition')

            self.step()

            body = []
            while not self.tok.check(TokenType.RIGHT_PAREN):
                e = self.expr()
                if e.error:
                    return e
                body.append(e.result)

            if not self.tok.check(TokenType.RIGHT_PAREN):
                return self.errorresult('`)` expected after function definition')

            self.step()

            return ParseResult(FunctionDefinition(pos, name, args, body))
        elif self.tok.check(TokenType.IDENTIFIER): # it's a constant
            name = self.tok.value
            self.step()
            value = self.expr()
            if value.error:
                return value
            if not self.tok.check(TokenType.RIGHT_PAREN):
                return self.errorresult('`)` expected after constant definition')
            self.step()
            return ParseResult(ConstantDefinition(pos, name, value.result))
        else:
            return self.errorresult('invalid token in definition')



    def if_expr(self):
        pos = self.tok.pos
        self.step()
        condition = self.expr()
        if condition.error:
            return condition
        body = self.expr()
        if body.error:
            return body
        else_body = self.expr()
        if else_body.error:
            return else_body

        if not self.tok.check(TokenType.RIGHT_PAREN):
            return self.errorresult('`)` expected after if expression')

        self.step()

        return ParseResult(If(pos, condition.result, body.result, else_body.result))

    def cond_expr(self):
        return self.errorresult('conditional expression not implemented')

    def expr(self) -> ParseResult:
        if self.tok.check(TokenType.LEFT_PAREN):
            self.step()
            if self.tok.value == 'def':
                return self.def_expr()
            elif self.tok.value == 'if':
                return self.if_expr()
            elif self.tok.value == 'cond':
                return self.cond_expr()
            pos = self.tok.pos
            op = self.expr()
            if op.error:
                return op
            args = []
            while not self.tok.check(TokenType.RIGHT_PAREN):
                e = self.expr()
                if e.error:
                    return e
                args.append(e.result)
            self.step()
            return ParseResult(FunctionCall(pos, op.result, args))
        elif self.tok.check(TokenType.IDENTIFIER):
            tok = self.tok
            self.step()
            return ParseResult(IdentifierRef(tok.pos, tok.value))
        elif self.tok.check(TokenType.KEYWORD):
            tok = self.tok
            self.step()
            return ParseResult(Keyword(tok.pos, tok.value))
        elif self.tok.check(TokenType.NUMBER) or\
             self.tok.check(TokenType.STRING) or\
             self.tok.check(TokenType.CHAR):
            tok = self.tok
            self.step()
            return ParseResult(Literal(tok.pos, tok.value))
        else:
            return self.errorresult('Unknown expression')

    def parse(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.step()

        while not self.tok.check(TokenType.EOF):
            yield self.expr()
