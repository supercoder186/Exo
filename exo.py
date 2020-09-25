from context import Context
from interpreter import Interpreter
from interpreter import SymbolTable
from lexer import Lexer
from exo_classes import Number
from parser import Parser

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
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()

    context = Context('<program>')
    context.symbol_table = global_symbol_table
    
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
