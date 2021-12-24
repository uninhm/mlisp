from enum import Enum
from dataclasses import dataclass

KEYWORDS = {
    'idx', 'len', 'input', 'print', 'div', 'mod', 'def',
    'if', 'cond', 'or', 'and', 'not',
    '+', '-', '*', '/', '=', '<', '>'
}

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
    CHAR = 'CHAR'

    KEYWORD = 'KEYWORD'

    # End of file.
    EOF = 'EOF'

class UnexpectedEOF(RuntimeError):
    pass

@dataclass
class Pos:
    filename: str
    line: int
    column: int

    def __str__(self):
        return f'{self.filename}:{self.line}:{self.column}'

class Token:
    def __init__(self, type: TokenType, pos: Pos, value=None):
        self.type: TokenType = type
        self.pos: Pos = pos
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
    
    def check(self, tokentype):
        if self.type == TokenType.EOF != tokentype:
            raise UnexpectedEOF()
        return self.type == tokentype

class Lexer:
    def current_pos(self):
        return Pos(self.filename, self.line, self.col)

    def step(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
            if self.char == '\n':
                self.line += 1
                self.col = 0
            else:
                self.col += 1
        else:
            self.char = 'EOF'
    
    def make_tokens(self, filename, text):
        self.filename = filename
        self.text = text
        self.line = 1
        self.col = 0
        self.idx = -1
        self.step()

        tokens = []
        while self.char != 'EOF':
            if self.char in ' \t\n':
                self.step()
            elif self.char == '(':
                tokens.append(Token(TokenType.LEFT_PAREN, self.current_pos()))
                self.step()
            elif self.char == ')':
                tokens.append(Token(TokenType.RIGHT_PAREN, self.current_pos()))
                self.step()
            elif self.char.isdigit():
                num = ''
                while self.char.isdigit() or self.char == '.':
                    num += self.char
                    self.step()
                if '.' in num:
                    tokens.append(Token(TokenType.NUMBER, self.current_pos(), float(num)))
                else:
                    tokens.append(Token(TokenType.NUMBER, self.current_pos(), int(num)))
            elif self.char == '"':
                string = ''
                self.step()
                while self.char != '"':
                    string += self.char
                    self.step()
                self.step()
                tokens.append(Token(TokenType.STRING, self.current_pos(), string))
            elif self.char == '?':
                self.step()
                char = self.char
                self.step()
                tokens.append(Token(TokenType.CHAR, self.current_pos(), ord(char)))
            else:
                ident = ''
                while self.char not in ' \t\n()' and self.char != 'EOF':
                    ident += self.char
                    self.step()
                kind = TokenType.IDENTIFIER
                if ident in KEYWORDS:
                    kind = TokenType.KEYWORD
                tokens.append(Token(kind, self.current_pos(), ident))

        tokens.append(Token(TokenType.EOF, self.current_pos()))
        return tokens
