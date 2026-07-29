import sys
from PIL import Image, ImageOps

def main():
    if len(sys.argv) != 3:
        sys.exit("Invalid arguments.")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    valid_extensions = (".jpg", ".jpeg", ".png")

    if (
        not input_file.lower().endswith(valid_extensions)
        or not output_file.lower().endswith(valid_extensions)
        or input_file.lower().split(".")[-1] != output_file.lower().split(".")[-1]
    ):
        sys.exit("Invalid arguments.")

    try:
        shirt = Image.open("shirt.png")
    except FileNotFoundError:
        sys.exit("Could not find shirt.png")

    try:
        with Image.open(input_file) as im:
            im = ImageOps.fit(im, shirt.size)
            im.paste(shirt, shirt)
            im.save(output_file)
    except FileNotFoundError:
        sys.exit("File does not exist.")

if __name__ == "__main__":
    main()
