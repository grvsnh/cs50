items = {}
while True:
    try:
        item = input().strip()
        if not item:
            continue
        item = item.upper()
        if item in items:
            items[item] += 1
        else:
            items[item] = 1
    except EOFError:
        break

for item in sorted(items):
    print(f"{items[item]} {item}")
