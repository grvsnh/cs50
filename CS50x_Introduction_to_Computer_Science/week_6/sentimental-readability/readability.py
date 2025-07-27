from cs50 import get_string


def count_letters(text):
    # Count only alphabetic characters
    return sum(1 for c in text if c.isalpha())


def count_words(text):
    # Words are separated by spaces, so words = spaces + 1
    return len(text.split())


def count_sentences(text):
    # Sentences end with ., !, or ?
    return sum(1 for c in text if c in ['.', '!', '?'])


def main():
    text = get_string("Text: ")

    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)

    # L = average number of letters per 100 words
    L = (letters / words) * 100
    # S = average number of sentences per 100 words
    S = (sentences / words) * 100

    # Coleman-Liau index formula
    index = 0.0588 * L - 0.296 * S - 15.8
    grade = round(index)

    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


if __name__ == "__main__":
    main()
