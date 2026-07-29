def main():
    text = input("Input: ")
    print("Output:", shorten(text))

def shorten(word):
    vowels = "aeiou"
    result = ""
    for ch in word:
        if ch.lower() not in vowels:
            result += ch
    return result

if __name__ == "__main__":
    main()
