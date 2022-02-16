from exo_language.exo_utils import exo_runner
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
    from exo_language import __version__
    print('Exo v' + __version__)

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

if __name__ == '__main__':
    main()