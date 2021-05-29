from .exo_utils import exo_runner
import sys
import os

def shell():
    while True:
        text = input('Exo >>> ')
        value, error = exo_runner.run('<stdin>', text)
        if error:
            print(error.as_string())
        elif value.value:
            print(value)

def main():
    args = sys.argv
    len_args = len(args)

    if len_args > 2:
        print('Too many arguments were supplied!')
    elif len_args < 2:
        shell()
    else:
        filename = os.path.abspath(args[1])

        with open(filename) as file:
            code = file.read()

        _value, error = exo_runner.run(filename, code)
        if error:
            print(error.as_string())
