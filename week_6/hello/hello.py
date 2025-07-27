from cs50 import get_string


def main():
    # Prompt the user for their name and store it in the variable 'name'
    name = get_string("Name: ")

    # Print a greeting message with the user's name
    print(f"hello, {name}")


# Ensures that main() runs only when this script is executed directly (not when imported as a module)
if __name__ == "__main__":
    main()
