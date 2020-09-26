import exo_token
from errors import RTError
from exo_classes import Number, Function


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    @staticmethod
    def visit_NumberNode(node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res

        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.type == exo_token.TT_PLUS:
            result, error = left.add_to(right), None
        elif node.op_tok.type == exo_token.TT_MINUS:
            result, error = left.sub_by(right), None
        elif node.op_tok.type == exo_token.TT_MUL:
            result, error = left.multiply_with(right), None
        elif node.op_tok.type == exo_token.TT_DIV:
            result, error = left.divide_by(right)
        elif node.op_tok.type == exo_token.TT_POW:
            result, error = left.power_by(right), None
        elif node.op_tok.type == exo_token.TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == exo_token.TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == exo_token.TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == exo_token.TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == exo_token.TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == exo_token.TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(exo_token.TT_KEYWORD, 'and'):
            result, error = left.and_by(right)
        elif node.op_tok.matches(exo_token.TT_KEYWORD, 'or'):
            result, error = left.or_by(right)
        else:
            result = 0
            error = None

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))

        if res.error:
            return res

        error = None
        if node.op_tok.type == exo_token.TT_MINUS:
            number, error = number.multiply_with(Number(-1)), None
        elif node.op_tok.matches(exo_token.TT_KEYWORD, 'not'):
            number, error = number.self_not()

        if error:
            return res.failure(error)
        else:
            return res.success(number)

    @staticmethod
    def visit_VarAccessNode(node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if value is None:
            return res.failure(RTError(
                node.pos_start, node.pos_end, f"'{var_name} is not defined'", context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_IfNode(self, node, context):
        res = RTResult()
        for condition, statements in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error:
                return res

            if not condition_value == 0:
                for statement in statements:
                    res.register(self.visit(statement, context))
                    if res.error:
                        return res

        if node.else_case:
            for statement in node.else_case:
                res.register(self.visit(statement, context))
                if res.error:
                    return res

        return res.success(None)

    def visit_WhileNode(self, node, context):
        res = RTResult()
        condition_value = res.register(self.visit(node.condition, context))

        while not condition_value.value == 0:
            for statement in node.body_nodes:
                res.register(self.visit(statement, context))
                if res.error:
                    return res

            condition_value = res.register(self.visit(node.condition, context))

        return res.success(None)

    @staticmethod
    def visit_FunctionDefNode(node, context):
        res = RTResult()
        name = node.fun_name_tok.value
        body_nodes = node.body_nodes
        return_node = node.return_node
        arg_names = (arg_name.value for arg_name in node.arg_name_toks)
        function_var = Function(name, body_nodes, arg_names, return_node)

        context.symbol_table.set(name, function_var)
        return res.success(function_var)


class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error:
            self.error = res.error

        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self
