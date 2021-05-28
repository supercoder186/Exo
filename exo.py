import exo_lang.exo_runner as exo_runner
import sys
import os

args = sys.argv
len_args = len(args)


if len_args > 2:
    print('Too many arguments were supplied!')
    sys.argv[1]
elif len_args < 2:
    print('No filename argument provided, reverting to test.exo')
    fn = 'test.exo'
else:
    fn = os.path.abspath(sys.argv[1])

with open(fn) as file:
    code = file.read()

value, error = exo_runner.run(fn, code)
if error:
    print(error.as_string())
