months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

while True:
    date = input("Date: ").strip()
    if "/" in date:
        parts = date.split("/")
        if len(parts) == 3:
            try:
                month, day, year = map(int, parts)
                if 1 <= month <= 12 and 1 <= day <= 31:
                    print(f"{year:04d}-{month:02d}-{day:02d}")
                    break
            except ValueError:
                pass
    elif "," in date:
        try:
            month_day, year = date.split(",")
            month_name, day = month_day.strip().split()
            month = months.index(month_name) + 1
            day, year = int(day), int(year)
            if 1 <= month <= 12 and 1 <= day <= 31:
                print(f"{year:04d}-{month:02d}-{day:02d}")
                break
        except (ValueError, IndexError):
            pass
