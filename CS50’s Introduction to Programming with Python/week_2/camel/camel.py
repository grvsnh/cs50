camel = input("camelCase: ").strip()

snake = ""
for i, ch in enumerate(camel):
    if ch.isupper():
        if i != 0:
            snake += "_"
        snake += ch.lower()
    else:
        snake += ch

print("snake_case:", snake)
