from datetime import date
import inflect
import sys


def get_total_minutes(birth_date, today):
    return (today - birth_date).days * 24 * 60


def main():
    try:
        birth_date = date.fromisoformat(input("Date of Birth: "))
    except ValueError:
        sys.exit("Invalid input.")

    minutes = get_total_minutes(birth_date, date.today())
    p = inflect.engine()
    words = p.number_to_words(minutes, andword='')
    words = words[0].upper() + words[1:]
    print(f"{words} {p.plural('minute', minutes)}")


if __name__ == "__main__":
    main()
