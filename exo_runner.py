from exo_classes import Number, BuiltInFunction
from exo_context import Context
from exo_interpreter import Interpreter
from exo_interpreter import SymbolTable
from exo_lexer import Lexer
from exo_parser import Parser

global_symbol_table = SymbolTable()
global_symbol_table.set('null', Number(0))
global_symbol_table.set('false', Number(0))
global_symbol_table.set('true', Number(1))
global_symbol_table.set("print", BuiltInFunction("print"))
global_symbol_table.set("input", BuiltInFunction("input"))
global_symbol_table.set("input_int", BuiltInFunction("input_int"))


def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast[-1].error:
        return None, ast[-1].error

    interpreter = Interpreter()

    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = None

    for statement in ast:
        result = interpreter.visit(statement.node, context)

    if result:
        return result.value, result.error
    else:
        return None
