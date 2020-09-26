import string

TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_POW = 'POW'
TT_EQ = 'EQ'
TT_EE = 'EE'
TT_NE = 'NE'
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'
TT_EOF = 'EOF'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LCPAREN = 'LCPAREN'
TT_RCPAREN = 'RCPAREN'
TT_COMMA = 'COMMA'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_TYPE = 'TYPE'
COMPARISONS = ('EE', 'NE', 'LT', 'GT', 'LTE', 'GTE')
DIGITS = '0123456789'
LETTERS = string.ascii_letters
ALPHANUMERIC = DIGITS + LETTERS
KEYWORDS = [
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'while',
    'fun',
    'return'
]
TYPES = [
    'var',
    'float',
    'int',
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
