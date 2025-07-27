def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if 1 <= height <= 8:
                return height
        except ValueError:
            pass  # Ignore non-integer input
        # No print for invalid input per specification; keep re-prompting


def main():
    height = get_height()
    for row in range(1, height + 1):
        # Left pyramid: spaces then hashes
        left = " " * (height - row) + "#" * row
        # Right pyramid: hashes
        right = "#" * row
        print(f"{left}  {right}")


if __name__ == "__main__":
    main()
