from ..exo_classes.exo_context import Context
from ..exo_errors.exo_errors import RTError

TT_VAR = 'var'
TT_INT = 'int'
TT_FLOAT = 'float'
TT_STRING = 'string'
TT_FUNCTION = 'fun'
TT_LIST = 'list'


class Value:
    def __init__(self):
        self.pos_start = None
        self.pos_end = None
        self.context = None
        self.type = None

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
        from ..exo_utils.exo_interpreter import RTResult
        return RTResult().failure(self.illegal_operation())

    def get_index(self, index):
        return None, self.illegal_operation()

    def set_index(self, index, value):
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
        self.type = TT_INT if isinstance(self.value, int) else TT_FLOAT

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
        self.type = TT_STRING
        self.pos_start = None
        self.pos_end = None
        self.context = None

    def add_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        elif isinstance(other, Number):
            return String(self.value + str(other.value)).set_context(self.context), None
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

    def get_index(self, index):
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
        self.type = TT_LIST
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

    def get_index(self, index):
        pos_start = index.pos_start
        pos_end = index.pos_end
        if not isinstance(index, Number):
            return None, self.illegal_operation(index)

        if index.value >= len(self.value) or index.value < 0:
            return None, RTError(pos_start, pos_end, 'Index out of bounds!', self.context)

        return self.value[index.value].set_context(self.context), None

    def set_index(self, index, value):
        from ..exo_utils.exo_interpreter import RTResult
        res = RTResult()
        pos_start = index.pos_start
        pos_end = index.pos_end
        if not isinstance(index, Number):
            return res.failure(self.illegal_operation(index))

        if index.value > len(self.value) or index.value < 0:
            return res.failure(RTError(pos_start, pos_end, 'Index out of bounds!', self.context))

        if index.value == len(self.value):
            self.value.append(value.value)
        else:
            self.value[index.value] = value.value

        return res.success(List(self.value).set_context(self.context))

    def __repr__(self):
        return str(self.value)


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"
        self.type = TT_FUNCTION

    def generate_new_context(self):
        from ..exo_utils.exo_interpreter import SymbolTable
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_types, arg_names, args):
        from ..exo_utils.exo_interpreter import RTResult
        res = RTResult()

        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))

        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))

        for i in range(len(args)):
            if arg_types[i] != 'var' and arg_types[i] != args[i].type:
                return res.failure(RTError(
                    self.pos_start, self.pos_end, 
                    f"Expected argument of type {arg_types[i]} but recieved {args[i].type}",
                    self.context
                ))

        return res.success(None)

    @staticmethod
    def populate_args(arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, None, arg_value, None)

    def check_and_populate_args(self, arg_types, arg_names, args, exec_ctx):
        from ..exo_utils.exo_interpreter import RTResult
        res = RTResult()
        res.register(self.check_args(arg_types, arg_names, args))
        if res.error:
            return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)


class Function(BaseFunction):
    def __init__(self, name, type, body_nodes, arg_types, arg_names, return_node):
        super().__init__(name)
        self.name = name or "<anonymous>"
        self.type = type
        self.body_nodes = body_nodes
        self.return_node = return_node
        self.arg_types = arg_types
        self.arg_names = arg_names

    def execute(self, args):
        from ..exo_utils.exo_interpreter import Interpreter, RTResult
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        exec_ctx.display_name = self.name
        res.register(self.check_and_populate_args(self.arg_types, self.arg_names, args, exec_ctx))
        if res.error:
            return res

        for node in self.body_nodes:
            res.register(interpreter.visit(node, exec_ctx))

            if res.error:
                return res
        
        value = interpreter.visit(self.return_node, exec_ctx)
        if isinstance(value, RTResult):
            value = res.register(value)
            if res.error:
                return res

        if self.type and self.type != value.type:
            return res.failure(RTError(self.pos_start, self.pos_end,\
                f'Expected type of {self.type} but recieved value of type {value.type}', exec_ctx))
        
        return res.success(value)


    def copy(self):
        copy = Function(self.name, self.type, self.body_nodes, self.arg_types, self.arg_names, self.return_node)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"


class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        from ..exo_utils.exo_interpreter import RTResult
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        arg_types = ['var'] * len(method.arg_names)

        res.register(self.check_and_populate_args(arg_types, method.arg_names, args, exec_ctx))
        if res.error:
            return res

        return_value = res.register(method(exec_ctx))
        if res.error:
            return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    def execute_print(self, exec_ctx):
        from ..exo_utils.exo_interpreter import RTResult
        print(str(exec_ctx.symbol_table.get('value')))
        return RTResult().success(Number(0))

    execute_print.arg_names = ['value']

    # noinspection PyUnusedLocal
    def execute_input(self, exec_ctx):
        from ..exo_utils.exo_interpreter import RTResult
        text = input()
        return RTResult().success(String(text))

    execute_input.arg_names = []

    # noinspection PyUnusedLocal
    def execute_input_int(self, exec_ctx):
        from ..exo_utils.exo_interpreter import RTResult
        while True:
            text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))

    execute_input_int.arg_names = []

    def execute_mod(self, exec_ctx):
        from ..exo_utils.exo_interpreter import RTResult
        x = exec_ctx.symbol_table.get('x')
        y = exec_ctx.symbol_table.get('y')
        types = ['int', 'float']
        if not (x.type in types and y.type in types):
            return RTResult().failure(RTError(x.pos_start, y.pos_end, 'Illegal types! Only int and float are allowed', exec_ctx))
        
        return RTResult().success(Number(x.value % y.value))

    execute_mod.arg_names = ['x', 'y']
