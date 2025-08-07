import sys
import csv
from tabulate import tabulate

if len(sys.argv) > 2:
    sys.exit("Too many command-line arguments")
elif len(sys.argv) < 2:
    sys.exit("Too few command-line arguments")

if not sys.argv[1].endswith(".csv"):
    sys.exit("Not a CSV file")

file_name = sys.argv[1]

if file_name.lower() == "sicilian.csv":
    pizza_col = "Sicilian Pizza"
elif file_name.lower() == "regular.csv":
    pizza_col = "Regular Pizza"
else:
    pizza_col = None

rows = []

try:
    with open(file_name) as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        if pizza_col:
            headers = [pizza_col if h in ("Sicilian Pizza", "Regular Pizza") else h for h in headers]
        rows.append(headers)

        for row in reader:
            if pizza_col:
                rows.append([row[pizza_col], row["Small"], row["Large"]])
            else:
                # If unknown CSV, append all columns in original order
                rows.append([row[h] for h in headers])

        print(tabulate(rows, headers="firstrow", tablefmt="grid"))

except FileNotFoundError:
    sys.exit("File does not exist")
