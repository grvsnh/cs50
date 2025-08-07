import random

while True:
    try:
        level = int(input("Level: "))
        if level <= 0:
            continue
        break
    except ValueError:
        continue

number = random.randint(1, level)

while True:
    try:
        guess = int(input("Guess: "))
        if guess <= 0:
            continue
        if guess < number:
            print("Too small!")
        elif guess > number:
            print("Too large!")
        else:
            print("Just right!")
            break
    except ValueError:
        continue
