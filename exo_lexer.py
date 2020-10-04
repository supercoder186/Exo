import exo_token
from exo_errors import IllegalCharError, ExpectedCharError
from exo_token import ALPHANUMERIC, DIGITS, KEYWORDS, TYPES, LETTERS, Token


class Lexer:
    def __init__(self, file_name, text):
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in '\t' or self.current_char in ' ':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in '"':
                tokens.append(self.make_string())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(Token(exo_token.TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(exo_token.TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(exo_token.TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(exo_token.TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(exo_token.TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(exo_token.TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(exo_token.TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(exo_token.TT_LCPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(exo_token.TT_RCPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(exo_token.TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error:
                    return [], error

                tokens.append(tok)
            elif self.current_char == '=':
                tokens.append(self.make_operator(exo_token.TT_EQ, exo_token.TT_EE))
            elif self.current_char == '<':
                tokens.append(self.make_operator(exo_token.TT_LT, exo_token.TT_LTE))
            elif self.current_char == '>':
                tokens.append(self.make_operator(exo_token.TT_GT, exo_token.TT_GTE))
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, ("'" + char + "'"))

        tokens.append(Token(exo_token.TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break

                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return Token(exo_token.TT_INT, int(num_str), pos_start, self.pos.copy())
        else:
            return Token(exo_token.TT_FLOAT, float(num_str), pos_start, self.pos.copy())

    def make_string(self):
        val_str = ''
        pos_start = self.pos.copy()
        self.advance()
        while self.current_char != '"':
            if self.current_char is None:
                return None, ExpectedCharError(pos_start, self.pos, 'Expected end of string, reached EOF')

            val_str += self.current_char
            self.advance()

        self.advance()
        return Token(exo_token.TT_STRING, val_str, pos_start, self.pos.copy())

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in ALPHANUMERIC + '_':
            id_str += self.current_char
            self.advance()

        if id_str in KEYWORDS:
            tok_type = exo_token.TT_KEYWORD
        elif id_str in TYPES:
            tok_type = exo_token.TT_TYPE
        else:
            tok_type = exo_token.TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos.copy())

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(exo_token.TT_NE, pos_start=pos_start, pos_end=self.pos.copy()), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_operator(self, tt_a, tt_b):
        tok_type = tt_a
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = tt_b

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos.copy())


class Position:
    def __init__(self, idx, ln, col, file_name, file_text):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.file_name = file_name
        self.file_text = file_text

    def __repr__(self):
        return f'In file {self.file_name} on line {self.ln + 1} column {self.col}'

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.file_name, self.file_text)
