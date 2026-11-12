"""
Lab 7 - Fixed laundry_service.py (hardened against fuzzed input)
Name : Purav N Khincha
SRN  : PES1UG24CS349

Every function now validates its input and returns None for anything
invalid instead of crashing or returning a nonsensical value.
"""
import math

GST_RATE = 1.18
MAX_INPUT_LEN = 1000  # guards against very large inputs (DoS)


def _to_float(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(value):  # rejects nan, inf, -inf, 1e400
        return None
    return value


def parse_order(text):
    """'garment:kg' -> (Garment, kg) or None if invalid."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LEN:
        return None
    parts = text.split(':')
    if len(parts) != 2:  # missing or extra ':'
        return None
    garment = parts[0].strip()
    if not garment or not garment.replace(' ', '').isalpha():
        return None
    kg = _to_float(parts[1].strip())
    if kg is None or kg <= 0:  # weight must be positive
        return None
    return garment.title(), kg


def weight_average(weights_csv):
    """'3,5,8' -> average weight (2 d.p.) or None if invalid."""
    if not isinstance(weights_csv, str) or len(weights_csv) > MAX_INPUT_LEN:
        return None
    values = []
    for raw in weights_csv.split(','):
        raw = raw.strip()
        if not raw:  # empty element e.g. '3,,5' or ''
            return None
        try:
            value = int(raw)
        except ValueError:  # non-numeric / too many digits
            return None
        if value <= 0:  # weights must be positive
            return None
        values.append(value)
    if not values:
        return None
    return round(sum(values) / len(values), 2)  # true division, not //


def payable_charge(text):
    """'charge|discount' -> charge * 1.18 - discount (min 0, 2 d.p.) or None."""
    if not isinstance(text, str) or len(text) > MAX_INPUT_LEN:
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    charge = _to_float(parts[0].strip())
    discount = _to_float(parts[1].strip())
    if charge is None or discount is None:
        return None
    if charge < 0 or discount < 0:  # negative discount would raise the bill
        return None
    total = charge * GST_RATE - discount
    if not math.isfinite(total):  # overflow, e.g. 1e308 * 1.18
        return None
    return round(max(total, 0), 2)


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter garment:weight in kg (e.g. regular:6): ")
    result = parse_order(user_input)
    if result is None:
        print("Invalid input! Use the format garment:weight with a positive weight.")
    else:
        print("Garment and Weight:", result)

    print("\n==== Running weight_average ====")
    user_input = input("Enter garment weights as CSV (e.g. 3,5,8): ")
    result = weight_average(user_input)
    if result is None:
        print("Invalid input! Enter positive whole numbers separated by commas.")
    else:
        print("Average Weight:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 300|40): ")
    result = payable_charge(user_input)
    if result is None:
        print("Invalid input! Use charge|discount with non-negative numbers.")
    else:
        print("Payable Charge:", result)


if __name__ == "__main__":
    main()
