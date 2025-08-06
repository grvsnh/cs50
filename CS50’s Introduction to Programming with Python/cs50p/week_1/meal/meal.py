def main():
    time = convert(input("What time is it? ").strip().lower())
    if 7 <= time <= 8:
        print("Breakfast time")
    elif 12 <= time <= 13:
        print("Lunch time")
    elif 18 <= time <= 19:
        print("Dinner time")
    else:
        print("No meal time")

def convert(time):
    # Normalize input: remove periods and spaces
    time = time.replace(".", "").strip()
    hours, minutes = map(int, time.replace("am", "").replace("pm", "").split(":"))
    if "pm" in time and hours != 12:
        hours += 12
    if "am" in time and hours == 12:
        hours = 0
    return hours + minutes / 60

if __name__ == "__main__":
    main()
