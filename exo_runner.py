from exo_context import Context
from exo_classes import Number
from exo_interpreter import Interpreter
from exo_interpreter import SymbolTable
from exo_lexer import Lexer
from exo_parser import Parser

global_symbol_table = SymbolTable()
global_symbol_table.set('null', Number(0))
global_symbol_table.set('false', Number(0))
global_symbol_table.set('true', Number(1))


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

    for statement in ast:
        result = interpreter.visit(statement.node, context)

    return result.value, result.error
