def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass  # Ignore non-integer inputs
        # Keep re-prompting silently for invalid input


def main():
    height = get_height()
    for row in range(1, height + 1):
        # Print spaces for left alignment, then the hashes
        spaces = " " * (height - row)
        hashes = "#" * row
        print(f"{spaces}{hashes}")


if __name__ == "__main__":
    main()
