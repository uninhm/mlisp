from enum import Enum

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'

    # Literals.
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'

    # End of file.
    EOF = 'EOF'

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer:
    def step(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
        else:
            self.char = 'EOF'
    
    def make_tokens(self, text):
        self.text = text
        self.idx = -1
        self.step()

        tokens = []
        while self.char != 'EOF':
            if self.char in ' \t\n':
                self.step()
            elif self.char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN))
                self.step()
            elif self.char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN))
                self.step()
            elif self.char.isdigit():
                num = ''
                while self.char.isdigit() or self.char == '.':
                    num += self.char
                    self.step()
                if '.' in num:
                    tokens.append(Token(TokenType.NUMBER, float(num)))
                else:
                    tokens.append(Token(TokenType.NUMBER, int(num)))
            else:
                ident = ''
                while self.char not in ' \t\n()' and self.char != 'EOF':
                    ident += self.char
                    self.step()
                tokens.append(Token(TokenType.IDENTIFIER, ident))

        return tokens