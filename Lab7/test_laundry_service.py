"""
Lab 7 - Fuzz Testing with Hypothesis
Name : Purav N Khincha
SRN  : PES1UG24CS349
Repo : L6_L7_41_laundry_service

Contract checked by these tests:
  * No function may ever raise an exception, whatever input it gets.
  * Invalid input  -> the function returns None.
  * Valid input    -> a sensible, finite result (no NaN / inf / negatives).
"""
import math

from hypothesis import given, settings, strategies as st
from laundry_service import parse_order, weight_average, payable_charge

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------
# Numbers as text, including nasty values float() happily accepts.
weird_numbers = st.one_of(
    st.floats(allow_nan=True, allow_infinity=True).map(str),
    st.integers().map(str),
    st.sampled_from(["nan", "inf", "-inf", "NaN", "1e400", "-0", "", " ", "abc", "1_000"]),
)
garment_names = st.one_of(
    st.text(max_size=12),
    st.sampled_from(["regular", "delicate", "bedding", "", "   "]),
)

# "garment:kg" shaped strings (random text alone rarely contains a ':')
order_like = st.builds(lambda g, k: f"{g}:{k}", garment_names, weird_numbers)
# "a,b,c" shaped strings, possibly with empty / non-numeric parts
csv_like = st.lists(weird_numbers, max_size=6).map(",".join)
# "charge|discount" shaped strings
charge_like = st.builds(lambda c, d: f"{c}|{d}", weird_numbers, weird_numbers)

ANY_INPUT = st.text() | st.none()


def _call(func, arg):
    try:
        return func(arg)
    except Exception as e:  # any exception is a bug
        raise AssertionError(f"{func.__name__}({arg!r}) crashed with {type(e).__name__}: {e}")


# ---------------------------------------------------------------------------
# parse_order
# ---------------------------------------------------------------------------
@given(ANY_INPUT)
def test_parse_order_no_crash(s):
    _call(parse_order, s)


@given(order_like)
def test_parse_order_structured_no_crash(s):
    result = _call(parse_order, s)
    if result is not None:
        garment, kg = result
        assert garment.strip() != "", f"empty garment accepted for {s!r}"
        assert math.isfinite(kg) and kg > 0, f"invalid weight {kg!r} accepted for {s!r}"


@given(st.sampled_from(["regular", "delicate", "bedding"]),
       st.floats(min_value=0.1, max_value=100, allow_nan=False))
def test_parse_order_valid(garment, kg):
    assert parse_order(f"{garment}:{kg}") == (garment.title(), kg)


# ---------------------------------------------------------------------------
# weight_average
# ---------------------------------------------------------------------------
@given(ANY_INPUT)
def test_weight_average_no_crash(s):
    _call(weight_average, s)


@given(csv_like)
def test_weight_average_structured_no_crash(s):
    result = _call(weight_average, s)
    if result is not None:
        assert math.isfinite(result) and result > 0


@given(st.lists(st.integers(min_value=1, max_value=200), min_size=1, max_size=20))
def test_weight_average_correct(values):
    # must be the real mean, not a floor-divided one
    expected = round(sum(values) / len(values), 2)
    assert weight_average(",".join(map(str, values))) == expected


# ---------------------------------------------------------------------------
# payable_charge
# ---------------------------------------------------------------------------
@given(ANY_INPUT)
def test_payable_charge_no_crash(s):
    _call(payable_charge, s)


@given(charge_like)
def test_payable_charge_structured_no_crash(s):
    result = _call(payable_charge, s)
    if result is not None:
        assert math.isfinite(result) and result >= 0, f"bad charge {result!r} for {s!r}"


@given(st.floats(min_value=0, max_value=1e6), st.floats(min_value=0, max_value=1e6))
def test_payable_charge_valid(charge, discount):
    result = payable_charge(f"{charge}|{discount}")
    assert result == round(max(charge * 1.18 - discount, 0), 2)


@settings(max_examples=50)
@given(st.floats(min_value=0, max_value=1e6), st.floats(min_value=-1e6, max_value=-0.01))
def test_payable_charge_rejects_negative_discount(charge, discount):
    # a negative discount would silently increase the bill
    assert payable_charge(f"{charge}|{discount}") is None
