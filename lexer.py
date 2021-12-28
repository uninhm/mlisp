from enum import Enum
from dataclasses import dataclass

KEYWORDS = {
    '%', 'def',
    'if', 'cond', 'or', 'and', 'not',
    '+', '-', '*', '/', '=', '<', '>', 'syscall',
    'progn', 'include', 'reserve', 'set', 'setp', 'getp', 'addr',
    'var'
}

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'

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

class Param:
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ

    def __str__(self):
        return f'{self.name}:{self.typ}'

    def __repr__(self):
        return self.__str__()

class Token:
    def __init__(self, kind: TokenType, pos: Pos, value=None, typ=None):
        self.kind: TokenType = kind
        self.pos: Pos = pos
        self.value = value
        self.typ = typ

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.kind,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def check(self, tokentype):
        if self.kind == TokenType.EOF != tokentype:
            raise UnexpectedEOF()
        return self.kind == tokentype

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
                pos = self.current_pos()
                num = ''
                while self.char.isdigit() or self.char == '.':
                    num += self.char
                    self.step()
                if '.' in num:
                    tokens.append(Token(TokenType.NUMBER, pos, float(num)))
                else:
                    tokens.append(Token(TokenType.NUMBER, pos, int(num)))
            elif self.char == '"':
                pos = self.current_pos()
                string = ''
                self.step()
                while self.char != '"':
                    if self.char == '\\':
                        self.step()
                        if self.char == 'n':
                            string += '\n'
                        elif self.char == 't':
                            string += '\t'
                        elif self.char == '\\':
                            string += '\\'
                        elif self.char == '"':
                            string += '"'
                        else:
                            raise RuntimeError(f'Unknown escape sequence: \\{self.char}')
                    else:
                        string += self.char
                    self.step()
                self.step()
                tokens.append(Token(TokenType.STRING, pos, string))
            elif self.char == '?': #TODO: Find a better syntax for char literals
                pos = self.current_pos()
                self.step()
                char = self.char
                self.step()
                tokens.append(Token(TokenType.CHAR, pos, ord(char)))
            elif self.char == ';':
                while self.char != '\n':
                    self.step()
            else:
                pos = self.current_pos()
                ident = ''
                while self.char not in ' \t\n():' and self.char != 'EOF':
                    ident += self.char
                    self.step()
                if self.char == ':':
                    self.step()
                    typ = ''
                    while self.char not in ' \t\n()' and self.char != 'EOF':
                        typ += self.char
                        self.step()
                    tokens.append(Token(TokenType.IDENTIFIER, pos, ident, typ))
                else:
                    kind = TokenType.IDENTIFIER
                    if ident in KEYWORDS:
                        kind = TokenType.KEYWORD
                    tokens.append(Token(kind, pos, ident))

        tokens.append(Token(TokenType.EOF, self.current_pos()))
        return tokens
