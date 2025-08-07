def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if len(s) < 2 or len(s) > 6:
        return False
    if not s[0].isalpha() or not s[1].isalpha():
        return False
    if not all(ch.isalnum() for ch in s):
        return False

    digit_started = False
    for ch in s:
        if ch.isdigit():
            if ch == "0" and not digit_started:
                return False
            digit_started = True
        elif digit_started and ch.isalpha():
            return False

    return True


if __name__ == "__main__":
    main()
