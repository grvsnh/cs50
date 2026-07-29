import re

def main():
    print(convert(input("Hours: ")))

def convert(s):
    pattern = r"^(\d{1,2})(?::(\d{2}))? (AM|PM) to (\d{1,2})(?::(\d{2}))? (AM|PM)$"
    match = re.match(pattern, s, flags=re.IGNORECASE)
    if not match:
        raise ValueError

    st_hour, st_min, st_ap, ed_hour, ed_min, ed_ap = match.groups()
    st_min = st_min if st_min else "00"
    ed_min = ed_min if ed_min else "00"
    st_hour, st_min, ed_hour, ed_min = map(int, [st_hour, st_min, ed_hour, ed_min])
    st_ap = st_ap.upper()
    ed_ap = ed_ap.upper()

    if not (1 <= st_hour <= 12) or not (0 <= st_min < 60):
        raise ValueError
    if not (1 <= ed_hour <= 12) or not (0 <= ed_min < 60):
        raise ValueError

    if st_ap == "AM":
        if st_hour == 12:
            st_hour = 0
    else:
        if st_hour != 12:
            st_hour += 12

    if ed_ap == "AM":
        if ed_hour == 12:
            ed_hour = 0
    else:
        if ed_hour != 12:
            ed_hour += 12

    return f"{st_hour:02d}:{st_min:02d} to {ed_hour:02d}:{ed_min:02d}"

if __name__ == "__main__":
    main()
