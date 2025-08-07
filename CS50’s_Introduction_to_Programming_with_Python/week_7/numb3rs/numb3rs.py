import re
import sys


def main():
    ip = input("IPv4 Address: ")
    print(validate(ip))


def validate(ip):
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip):
        return False

    parts = ip.split(".")
    for part in parts:
        if len(part) > 1 and part.startswith("0"):
            return False
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False

    return True


if __name__ == "__main__":
    main()
