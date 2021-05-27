import exo_lang.exo_runner as exo_runner

while True:
    text = input('Exo >>> ')
    value, error = exo_runner.run('<stdin>', text)
    if error:
        print(error.as_string())
