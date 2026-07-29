from cs50 import get_string


def main():
    card_number = get_string("Number: ")

    # Check if card_number contains only digits
    if not card_number.isdigit():
        print("INVALID")
        return

    if not luhn_check(card_number):
        print("INVALID")
        return

    # Determine card type based on starting digits and length
    if (len(card_number) == 15 and
            (card_number.startswith("34") or card_number.startswith("37"))):
        print("AMEX")
    elif (len(card_number) == 16 and
          51 <= int(card_number[:2]) <= 55):
        print("MASTERCARD")
    elif (len(card_number) in [13, 16] and
          card_number.startswith("4")):
        print("VISA")
    else:
        print("INVALID")


def luhn_check(number):
    """Implements Luhn’s algorithm to validate a credit card number."""

    total = 0
    num_digits = len(number)
    parity = num_digits % 2

    for i, digit_char in enumerate(number):
        digit = int(digit_char)

        # Double every other digit starting from second-to-last digit
        if i % 2 == parity:
            digit *= 2
            # If doubling results in a number greater than 9, subtract 9
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


if __name__ == "__main__":
    main()
