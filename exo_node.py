class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node} {self.op_tok} {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = var_name_tok.pos_start
        self.pos_end = var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = var_name_tok.pos_start
        self.pos_end = value_node.pos_end


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        if self.else_case:
            self.pos_end = self.else_case[1][-1].pos_end
        else:
            if self.cases[-1][1]:
                self.pos_end = self.cases[-1][1][-1].pos_end
            else:
                self.pos_end = self.cases[-1][0].pos_end


class WhileNode:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

        self.pos_start = self.condition.pos_start
        self.pos_end = self.statements[-1].pos_end


class ForNode:
    def __init__(self, var_name_tok, start, stop, step, body_nodes):
        self.var_name_tok = var_name_tok
        self.start = start
        self.stop = stop
        self.step = step
        self.body_nodes = body_nodes

        self.pos_start = var_name_tok.pos_start
        self.pos_end = self.body_nodes[-1].pos_end


class FunctionDefNode:
    def __init__(self, fun_name_tok, arg_name_toks, body_nodes, return_node):
        self.fun_name_tok = fun_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_nodes = body_nodes
        self.return_node = return_node

        self.pos_start = fun_name_tok.pos_start
        self.pos_end = return_node.pos_end


class FunctionCallNode:
    def __init__(self, call_node, arg_nodes):
        self.call_node = call_node
        self.arg_nodes = arg_nodes
        self.pos_start = call_node.pos_start
        if len(arg_nodes) > 0:
            self.pos_end = arg_nodes[-1].pos_end
        else:
            self.pos_end = call_node.pos_end


class ReturnNode:
    def __init__(self, value_node):
        self.value_node = value_node
        self.pos_start = value_node.pos_start
        self.pos_end = value_node.pos_end
