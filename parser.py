import exo_token
from errors import InvalidSyntaxError
from exo_node import NumberNode, BinOpNode, UnaryOpNode, VarAssignNode, VarAccessNode, IfNode, WhileNode, \
    FunctionDefNode, FunctionCallNode, ReturnNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok = None
        self.advance()

    def parse(self):
        res = self.statement()
        if not res.error and self.current_tok.type != exo_token.TT_EOF:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  'Expected an operation'))
        return res

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())

        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def parse_braces(self):
        res = ParseResult()
        res.register_advance()
        self.advance()

        if self.current_tok.type != exo_token.TT_LCPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected '{'"))

        res.register_advance()
        self.advance()

        statements = []
        while self.current_tok.type != exo_token.TT_RCPAREN:
            statement = res.register(self.statement())
            if res.error:
                return res

            statements.append(statement)

        res.register_advance()
        self.advance()
        return res.success(statements)

    def parse_conditional_statement(self):
        res = ParseResult()
        res.register_advance()
        self.advance()

        if self.current_tok.type != exo_token.TT_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected '('"))

        res.register_advance()
        self.advance()
        condition = res.register(self.num_expr())
        if res.error:
            return res

        if self.current_tok.type != exo_token.TT_RPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected ')'"))

        result = self.parse_braces()
        if result.error:
            return result

        return res.success((condition, result.node))

    def parse_args(self):
        res = ParseResult()
        res.register_advance()
        self.advance()

        arg_toks = []

        while self.current_tok.type != exo_token.TT_RPAREN:
            if self.current_tok.type != exo_token.TT_TYPE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, 'Expected variable type!'))
            res.register_advance()
            self.advance()
            if self.current_tok.type != exo_token.TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, 'Expected variable identifier!'))

            arg_toks.append(self.current_tok)
            res.register_advance()
            self.advance()

        return res.success(arg_toks)

    def statement(self):
        res = ParseResult()
        if self.current_tok.matches(exo_token.TT_KEYWORD, 'if'):
            statement = res.register(self.if_expr())
            if res.error:
                return res

            return res.success(statement)
        elif self.current_tok.matches(exo_token.TT_KEYWORD, 'while'):
            statement = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(statement)
        elif self.current_tok.type == exo_token.TT_TYPE or self.current_tok.matches(exo_token.TT_KEYWORD, 'return'):
            statement = res.register(self.expr())
            if res.error:
                return res
            return res.success(statement)
        elif self.current_tok.matches(exo_token.TT_KEYWORD, 'fun'):
            statement = res.register(self.function_def())
            if res.error:
                return res
            return res.success(statement)
        else:
            statement = res.register(self.num_expr())
            if res.error:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                       'Expected if, while, function def, variable assignment or numeric expression!'
                                       ), override=True)
            return res.success(statement)

    def function_def(self):
        res = ParseResult()
        res.register_advance()
        self.advance()
        if self.current_tok.type == exo_token.TT_TYPE:
            res.register_advance()
            self.advance()

        if self.current_tok.type != exo_token.TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  'Expected an identifier!'))

        fun_name_tok = self.current_tok
        res.register_advance()
        self.advance()

        if self.current_tok.type != exo_token.TT_LPAREN:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  "Expected an '('"))

        args_res = self.parse_args()
        if args_res.error:
            return args_res

        arg_toks = args_res.node

        statements_res = self.parse_braces()
        if statements_res.error:
            return statements_res

        statements = statements_res.node
        to_return = None

        for statement in statements:
            if type(statement) == ReturnNode:
                to_return = statement
                while statements[-1] != statement:
                    del statements[-1]
                del statements[-1]

        if to_return is None:
            to_return = NumberNode(exo_token.Token(exo_token.TT_INT, 0, statements[-1].pos_end, statements[-1].pos_end))

        return res.success(FunctionDefNode(fun_name_tok, arg_toks, statements, to_return))

    def if_expr(self):
        res = ParseResult()
        cases = []
        result = self.parse_conditional_statement()
        if result.error:
            return res.failure(result.error)

        cases.append(result.node)
        while self.current_tok.matches('KEYWORD', 'elif'):
            result = self.parse_conditional_statement()
            if result.error:
                return res.failure(result.error)

            cases.append(result.node)

        else_case = None
        if self.current_tok.matches('KEYWORD', 'else'):
            result = self.parse_braces()
            if result.error:
                return res.failure(result.error)

            else_case = result.node

        return res.success(IfNode(cases, else_case))

    def while_expr(self):
        res = ParseResult()
        result = self.parse_conditional_statement()
        if result.error:
            return res.failure(result.error)

        condition, statements = result.node
        return res.success(WhileNode(condition, statements))

    def expr(self):
        res = ParseResult()
        if self.current_tok.type == exo_token.TT_TYPE:
            res.register_advance()
            self.advance()
            if self.current_tok.type != exo_token.TT_IDENTIFIER:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, 'Expected an identifier'))

            var_name = self.current_tok

            res.register_advance()
            self.advance()
            if self.current_tok.type != exo_token.TT_EQ:
                return res.failure(
                    InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, 'Expected ='))

            res.register_advance()
            self.advance()
            expr = res.register(self.num_expr())
            if res.error:
                return res

            return res.success(VarAssignNode(var_name, expr))
        elif self.current_tok.matches(exo_token.TT_KEYWORD, 'return'):
            res.register_advance()
            self.advance()
            num_res = self.num_expr()
            if num_res.error:
                return num_res

            return res.success(ReturnNode(num_res.node))

    def num_expr(self):
        res = ParseResult()
        node = res.register(self.bin_op(self.comp_expr,
                                        ((exo_token.TT_KEYWORD, 'and'), (exo_token.TT_KEYWORD, 'or'))))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                  'Expected numeric expression'))

        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(exo_token.TT_KEYWORD, 'not'):
            op_tok = self.current_tok
            res.register_advance()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error:
                return res
            return res.success(UnaryOpNode(op_tok, node))
        else:
            node = res.register(self.bin_op(self.arith_expr, exo_token.COMPARISONS))

            if res.error:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                      "Expected value, 'not', +, - or ("))

            return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (exo_token.TT_PLUS, exo_token.TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (exo_token.TT_MUL, exo_token.TT_DIV))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (exo_token.TT_PLUS, exo_token.TT_MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res

            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def power(self):
        return self.bin_op(self.call, (exo_token.TT_POW,), self.factor)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_tok.type == exo_token.TT_LPAREN:
            res.register_advance()
            self.advance()
            arg_nodes = []

            if self.current_tok.type == exo_token.TT_RPAREN:
                res.register_advance()
                self.advance()
            else:
                arg_nodes.append(res.register(self.num_expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected numeric expression"
                    ))

                while self.current_tok.type == exo_token.TT_COMMA:
                    res.register_advance()
                    self.advance()

                    arg_nodes.append(res.register(self.num_expr()))
                    if res.error:
                        return res

                if self.current_tok.type != exo_token.TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advance()
                self.advance()
            return res.success(FunctionCallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (exo_token.TT_INT, exo_token.TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == exo_token.TT_IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == exo_token.TT_LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type == exo_token.TT_RPAREN:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end,
                                                      "Expected ')'"))

        return res.failure(InvalidSyntaxError(tok.pos_start, tok.pos_end, "Expected value, +, - or ("))


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advance(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error, override=False):
        if not self.error or self.advance_count == 0:
            self.error = error
        elif override:
            self.error = error
        return self
