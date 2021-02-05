import exo_runner

import sys

args = sys.argv
len_args = len(args)

fn = ''

if len_args > 2:
    print('Too many arguments were supplied!')
    sys.argv[1]
elif len_args < 2:
    print('No filename argument provided, reverting to test.exo')
    fn = 'test.exo'
else:
    fn = sys.argv[1]

with open(fn) as file:
    code = file.read()

value, error = exo_runner.run(fn, code)
if error:
    print(error.as_string())
