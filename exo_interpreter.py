import exo_token
from exo_classes import Number, String, List, Function
from exo_errors import RTError
from exo_node import VarAssignNode, NumberNode, StringNode, BinOpNode, UnaryOpNode, VarAccessNode, IfNode, WhileNode, ForNode, ReturnNode, FunctionDefNode, FunctionCallNode


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value[1]

    def set(self, name, type_tok, value, context):
        if type_tok:
            type = type_tok.value
        else:
            type = None

        if type == 'var':
            type = None
        
        var_type = None
        res = RTResult()
        if name in self.symbols:
            var_type = self.symbols[name][0]
        """
        if name in self.symbols and type is not None:
            var_type = self.symbols[name][0]
            if type != var_type and var_type is not None:
                return res.failure(RTError(type_tok.pos_start, type_tok.pos_end, \
                    f"Type mismatch! Referred to variable {name} of type {var_type} as {type}", context))

        if (type and value.type != type) or (var_type and value.type != var_type):
            return res.failure(RTError(type_tok.pos_start, type_tok.pos_end, \
                f"Type mismatch! Attempted to assign value of type {value.type} to var of type {type}", context))"""
        
        if name in self.symbols and type:
            if type != var_type and var_type:
                return res.failure(RTError(type_tok.pos_start, type_tok.pos_end, \
                    f"Type mismatch! Referred to variable {name} of type {var_type} as {type}", context))
    
            var_type = type
        
        if type and type != value.type:
            return res.failure(RTError(type_tok.pos_start, type_tok.pos_end, \
                    f"Type mismatch! Referred to value as type {type} but it is {value.type}", context))

        if var_type and var_type != value.type:
            return res.failure(RTError(type_tok.pos_start, type_tok.pos_end, \
                f"Type mismatch! Attempted to assign value of type {value.type} to var of type {var_type}", context))
        
        if var_type:
            self.symbols[name] = (var_type, value)
        else:
            self.symbols[name] = (type, value)
        return res.success(None)

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

    @staticmethod
    def visit_StringNode(node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_ListNode(self, node, context):
        res = RTResult()
        elms = node.elms
        processed_elms = []
        for elem in elms:
            processed_elem = res.register(self.visit(elem, context))
            processed_elms.append(processed_elem)

        return RTResult().success(
            List(processed_elms).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res

        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_tok.type == exo_token.TT_PLUS:
            result, error = left.add_to(right)
        elif node.op_tok.type == exo_token.TT_MINUS:
            result, error = left.sub_by(right)
        elif node.op_tok.type == exo_token.TT_MUL:
            result, error = left.multiply_with(right)
        elif node.op_tok.type == exo_token.TT_DIV:
            result, error = left.divide_by(right)
        elif node.op_tok.type == exo_token.TT_POW:
            result, error = left.power_by(right)
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

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if value is None:
            return res.failure(RTError(
                node.pos_start, node.pos_end, f"'{var_name} is not defined'", context
            ))

        if node.index_node:
            index_val = res.register(self.visit(node.index_node, context))
            if res.error:
                return res
            value, error = value.get_index(index_val)
            if error:
                return res.failure(error)

            value = value.set_pos(node.pos_start, node.pos_end)
        else:
            value = value.set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node: VarAssignNode, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))

        if node.index_node:
            list_val = context.symbol_table.get(var_name)
            index_val = res.register(self.visit(node.index_node, context))
            if res.error:
                return res

            if list_val is None:
                return res.failure(RTError(
                    node.pos_start, node.pos_end, f"'{var_name} is not defined'", context
                ))

            updated_list_val = res.register(list_val.set_index(index_val, value))
            if res.error:
                return res

            res.register(context.symbol_table.set(var_name, node.type_tok, updated_list_val, context))
            if res.error:
                return res
            
            return res.success(updated_list_val)
        else:
            if res.error:
                return res

            res.register(context.symbol_table.set(var_name, node.type_tok, value, context))
            if res.error:
                return res
            
            return res.success(value)

    def visit_IfNode(self, node, context):
        res = RTResult()
        for condition, statements in node.cases:
            condition_value = res.register(self.visit(condition))
            if res.error:
                return res

            if not condition_value.value == 0:
                for statement in statements:
                    res.register(self.visit(statement, context))
                    if res.error:
                        return res

                return res.success(None)

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

    def visit_ForNode(self, node: ForNode, context):
        res = RTResult()
        init_assignment_node = VarAssignNode(node.var_type_tok, node.var_name_tok, node.start)
        step_val = res.register(self.visit(node.step, context)).value
        if res.error:
            return res
        stop_val = res.register(self.visit(node.stop, context)).value
        if res.error:
            return res
        res.register(self.visit(init_assignment_node, context))
        if res.error:
            return res

        def var_val():
            return context.symbol_table.get(node.var_name_tok.value).value

        while abs(var_val()) < abs(stop_val):
            for statement in node.body_nodes:
                res.register(self.visit(statement, context))
                if res.error:
                    return res

            res.register(context.symbol_table.set(node.var_name_tok.value, var_type_tok, Number(var_val() + step_val), context))
            if res.error:
                return res

        return res.success(None)

    def visit_ReturnNode(self, node, context):
        return self.visit(node.value_node, context)

    @staticmethod
    def visit_FunctionDefNode(node: FunctionDefNode, context):
        res = RTResult()
        name = node.fun_name_tok.value
        body_nodes = node.body_nodes
        return_node = node.return_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        function_var = Function(name, body_nodes, arg_names, return_node).set_context(context) \
            .set_pos(node.pos_start, node.pos_end)

        context.symbol_table.set(name, None, function_var, None)
        return res.success(function_var)

    def visit_FunctionCallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.call_node, context))
        value_to_call.context = context
        if res.error:
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error:
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.error:
            return res
        return res.success(return_value)


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
