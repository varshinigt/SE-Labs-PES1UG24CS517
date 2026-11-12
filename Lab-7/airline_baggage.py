import math


def parse_booking(code):
    """Return (airline, flight_number, seat_letter) or None if invalid."""
    if not isinstance(code, str):
        return None
    parts = code.strip().split('-')
    if len(parts) != 3:
        return None
    airline, flight, seat = (p.strip() for p in parts)
    if not airline or not seat:
        return None
    try:
        flight_number = int(flight)
    except ValueError:
        return None
    return airline.upper(), flight_number, seat[-1].upper()


def total_weight(weights_csv):
    """Return total weight in kg, or None if the input is invalid."""
    if not isinstance(weights_csv, str):
        return None
    total = 0.0
    for w in weights_csv.split(','):
        try:
            value = float(w)
        except ValueError:
            return None
        if not math.isfinite(value) or value < 0:
            return None
        total += value
    return total


def tag_label(name):
    """Return 'F. LASTNAME', or None if the name is invalid."""
    if not isinstance(name, str):
        return None
    parts = name.split()
    if len(parts) < 2:
        return None
    return parts[0][0].upper() + '. ' + parts[-1].upper()


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    result = parse_booking(user_input)
    if result is None:
        print("Invalid booking code.")
    else:
        print("Airline, Flight and Seat Letter:", result)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    result = total_weight(user_input)
    if result is None:
        print("Invalid weights. Use non-negative numbers separated by commas.")
    else:
        print("Total Weight:", result)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    result = tag_label(user_input)
    if result is None:
        print("Invalid name. Enter both first and last name.")
    else:
        print("Tag Label:", result)


if __name__ == "__main__":
    main()
