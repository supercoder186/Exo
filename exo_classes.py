from exo_context import Context
from exo_errors import RTError


class Value:
    def __init__(self):
        self.pos_start = None
        self.pos_end = None
        self.context = None

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add_to(self, other):
        return None, self.illegal_operation(other)

    def sub_by(self, other):
        return None, self.illegal_operation(other)

    def multiply_with(self, other):
        return None, self.illegal_operation(other)

    def divide_by(self, other):
        return None, self.illegal_operation(other)

    def power_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def and_by(self, other):
        return None, self.illegal_operation(other)

    def or_by(self, other):
        return None, self.illegal_operation(other)

    def self_not(self):
        return None, self.illegal_operation()

    def execute(self, args):
        from exo_interpreter import RTResult
        return RTResult().failure(self.illegal_operation())

    def at_index(self, index):
        return None, self.illegal_operation()

    def copy(self):
        raise Exception('No copy method defined')

    @staticmethod
    def is_true():
        return False

    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def add_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multiply_with(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def divide_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def power_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def and_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def or_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def self_not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return str(self.value)


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.pos_start = None
        self.pos_end = None
        self.context = None

    def add_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def at_index(self, index):
        pos_start = index.pos_start
        pos_end = index.pos_end
        if not isinstance(index, Number):
            return None, self.illegal_operation(index)

        if index.value >= len(self.value) or index.value < 0:
            return None, RTError(pos_start, pos_end, 'Index out of bounds!', self.context)

        return String(self.value[index]).set_context(self.context), None

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return self.value


class List(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.pos_start = None
        self.pos_end = None
        self.context = None

    def add_to(self, other):
        if isinstance(other, List):
            return List(self.value + other.value).set_context(self.context), None
        else:
            return List(self.value.append(other)).set_context(self.context), None

    def sub_by(self, other):
        if isinstance(other, List):
            elms = other.value
            val_list = self.value
            for elem in elms:
                val_list.remove(elem.value)

            return List(val_list).set_context(self.context), None
        else:
            return List(self.value.remove(other.value)).set_context(self.context), None

    def get_comparison_eq(self, other):
        if isinstance(other, List):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        if isinstance(other, List):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, self.illegal_operation(other)

    def at_index(self, index):
        pos_start = index.pos_start
        pos_end = index.pos_end
        if not isinstance(index, Number):
            return None, self.illegal_operation(index)

        if index.value >= len(self.value) or index.value < 0:
            return None, RTError(pos_start, pos_end, 'Index out of bounds!', self.context)

        return List(self.value[index]).set_context(self.context), None

    def __repr__(self):
        return str(self.value)


class Function(Value):
    def __init__(self, name, body_nodes, arg_names, return_node):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_nodes = body_nodes
        self.return_node = return_node
        self.arg_names = arg_names

    def execute(self, args):
        from exo_interpreter import Interpreter, RTResult, SymbolTable
        res = RTResult()
        interpreter = Interpreter()
        fun_context = Context(self.name, self.context, self.pos_start)
        fun_context.symbol_table = SymbolTable(fun_context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(self.arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(self.arg_names) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(fun_context)
            fun_context.symbol_table.set(arg_name, arg_value)

        for node in self.body_nodes:
            interpreter.visit(node, fun_context)

        value = interpreter.visit(self.return_node, fun_context)
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_nodes, self.arg_names, self.return_node)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"
