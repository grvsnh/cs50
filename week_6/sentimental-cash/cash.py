from cs50 import get_float


def main():
    # Prompt user until a non-negative float is provided
    while True:
        try:
            change = get_float("Change owed: ")
            if change >= 0:
                break
        except ValueError:
            # If input cannot be converted to float, re-prompt
            pass

    # Convert dollars to cents (round to nearest cent)
    cents = round(change * 100)

    coins = 0
    for coin_value in [25, 10, 5, 1]:
        coins += cents // coin_value   # Number of coins of this denomination
        cents %= coin_value            # Remaining cents

    print(coins)


if __name__ == "__main__":
    main()
