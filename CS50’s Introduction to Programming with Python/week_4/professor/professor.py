import random

def main():
    level = get_level()
    score = 0
    for _ in range(10):
        x = generate_integer(level)
        y = generate_integer(level)
        score += check_answer(x, y)
    print("Score:", score)

def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level in [1, 2, 3]:
                return level
        except ValueError:
            continue

def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(100, 999)

def check_answer(x, y):
    attempts = 0
    while attempts < 3:
        try:
            answer = int(input(f"{x} + {y} = "))
            if answer == x + y:
                return 1
            else:
                print("EEE")
                attempts += 1
        except ValueError:
            continue
    print(f"{x} + {y} = {x + y}")
    return 0

if __name__ == "__main__":
    main()
