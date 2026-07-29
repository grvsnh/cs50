def take_input():
    while True:
        try:
            x_str, y_str = input("Fraction: ").split("/")
            x = int(x_str)
            y = int(y_str)
            if y == 0 or y < 0 or x < 0:
                raise ValueError
            if x > y:
                raise ValueError
            return round(x / y * 100)
        except (ValueError, ZeroDivisionError):
            pass

def main():
    percentage = take_input()
    if percentage <= 1:
        print("E")
    elif percentage >= 99:
        print("F")
    else:
        print(f"{percentage}%")

if __name__ == "__main__":
    main()
