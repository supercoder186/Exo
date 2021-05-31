import re

from ..exo_classes.exo_classes import BuiltInFunction, Number
from ..exo_classes.exo_context import Context
from ..exo_utils.exo_interpreter import Interpreter, SymbolTable
from ..exo_utils.exo_lexer import Lexer
from ..exo_utils.exo_parser import Parser

global_symbol_table = SymbolTable()
global_symbol_table.set('null', None, Number(0), None)
global_symbol_table.set('false', None, Number(0), None)
global_symbol_table.set('true', None, Number(1), None)
global_symbol_table.set("print", None, BuiltInFunction("print"), None)
global_symbol_table.set("input", None, BuiltInFunction("input"), None)
global_symbol_table.set("input_int", None, BuiltInFunction("input_int"), None)

def filter_comments(text):
    regexpr = r'[ ]*[#]+.*'
    text = re.sub(regexpr, '', text)
    return text

def run(file_name, text):
    text = filter_comments(text)
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
        if result.error:
            return result.value, result.error

    if result:
        return result.value, result.error
    else:
        return None
