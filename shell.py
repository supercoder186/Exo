import exo


while True:
    text = input('Exo >>> ')
    value, error = exo.run('<stdin>', text)
    if error:
        print(error.as_string())
    else:
        print(value)
