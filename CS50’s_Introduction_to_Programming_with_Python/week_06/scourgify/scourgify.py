import csv
import sys

if len(sys.argv) != 3:
    sys.exit("Too few/many command-line arguments")

input_file, output_file = sys.argv[1], sys.argv[2]

if not input_file.endswith(".csv") or not output_file.endswith(".csv"):
    sys.exit("Not a CSV file")

try:
    with open(input_file) as infile, open(output_file, "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=["first", "last", "house"])
        writer.writeheader()
        for row in reader:
            try:
                last, first = row["name"].split(", ")
            except ValueError:
                sys.exit("Invalid name format")
            writer.writerow({"first": first, "last": last, "house": row["house"]})
except FileNotFoundError:
    sys.exit(f"Could not read {input_file}")
