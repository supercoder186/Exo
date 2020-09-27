import exo_runner

while True:
    text = input('Exo >>> ')
    value, error = exo_runner.run('<stdin>', text)
    if error:
        print(error.as_string())
    else:
        print(value)
