import exo_runner

# fn = input('Enter file name: ')
fn = 'test.exo'

with open('test.exo') as file:
    code = file.read()
    code = code.replace('\n', ' ')

value, error = exo_runner.run(fn, code)
if error:
    print(error.as_string())
else:
    print(value)
