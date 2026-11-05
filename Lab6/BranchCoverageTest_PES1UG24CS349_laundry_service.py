"""
Lab 6 - Branch Coverage Tests
Name : Purav N Khincha
SRN  : PES1UG24CS349
Repo : L6_L7_41_laundry_service

Goal: make every decision (if / elif / and) in laundry_service.py
evaluate to both True and False (>= 90% branch coverage).
Includes boundary-value tests for each comparison.
"""
import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# =====================================================================
# extra_weight_charge
# =====================================================================

# --- validation branches ---
@pytest.mark.parametrize("garment", ["silk", "", "REGULAR"])
def test_unknown_garment_type_raises(garment):
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge(garment, 5, "standard", False)


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -0.5, "standard", False)


def test_zero_weight_is_valid():
    # weight_kg < 0 -> False branch at its boundary
    assert extra_weight_charge("regular", 0, "standard", False) == 0


# --- membership branch: (is_member and garment_type != "bedding") ---
def test_non_member_no_bonus():
    # is_member False -> 5 included, extra 1
    assert extra_weight_charge("regular", 6, "standard", False) == 30


def test_member_regular_bonus():
    # is_member True, not bedding -> 7 included, 6 kg is within
    assert extra_weight_charge("regular", 6, "standard", True) == 0


def test_member_delicate_bonus():
    # delicate 3 + 2 = 5 included -> extra 1 * 30
    assert extra_weight_charge("delicate", 6, "standard", True) == 30


def test_member_bedding_no_bonus():
    # is_member True but bedding -> condition False, stays 8 included
    assert extra_weight_charge("bedding", 10, "standard", True) == 60


# --- extra <= 0 branch (boundary) ---
def test_exactly_included_weight_is_free():
    assert extra_weight_charge("bedding", 8, "express", False) == 0


def test_just_over_included_weight():
    assert extra_weight_charge("bedding", 9, "standard", False) == 30


# --- speed branch: standard vs other ---
def test_standard_rate():
    assert extra_weight_charge("delicate", 5, "standard", False) == 60


def test_express_rate_small_extra():
    assert extra_weight_charge("delicate", 5, "express", False) == 100


def test_other_speed_uses_non_standard_rate():
    # any non-"standard" speed falls to the else branch (rate 50)
    assert extra_weight_charge("delicate", 5, "same_day", False) == 100


# --- extra > 10 branch and nested express branch ---
def test_extra_exactly_ten_no_surcharge():
    # extra = 10 -> extra > 10 is False
    assert extra_weight_charge("regular", 15, "standard", False) == 300


def test_heavy_standard_surcharge_only():
    # extra 11 -> rate 30 + 15 = 45 (nested express check False)
    assert extra_weight_charge("regular", 16, "standard", False) == 11 * 45


def test_heavy_express_surcharge():
    # extra 15 -> rate 50 + 15 + 10 = 75 (nested express check True)
    assert extra_weight_charge("regular", 20, "express", False) == 1125


def test_heavy_non_standard_non_express():
    # extra 11 -> rate 50 + 15 = 65 (not standard, not express)
    assert extra_weight_charge("regular", 16, "same_day", False) == 11 * 65


def test_heavy_member_bedding_express():
    # bedding stays 8 included even for member -> extra 12, rate 75
    assert extra_weight_charge("bedding", 20, "express", True) == 12 * 75


# =====================================================================
# order_acceptable
# =====================================================================
def test_delicate_within_item_limit():
    assert order_acceptable(5, 5, True) is True


def test_delicate_over_item_limit():
    assert order_acceptable(5, 6, True) is False


def test_delicate_ignores_weight_limit():
    # is_delicate returns before the weight check
    assert order_acceptable(100, 2, True) is True


def test_weight_at_limit_accepted():
    assert order_acceptable(25, 10, False) is True


def test_weight_over_limit_rejected():
    assert order_acceptable(25.1, 10, False) is False


def test_items_at_limit_accepted():
    assert order_acceptable(10, 40, False) is True


def test_items_over_limit_rejected():
    assert order_acceptable(10, 41, False) is False


# =====================================================================
# dropoff_status
# =====================================================================
# cutoff: bedding 90 / otherwise 60, +30 if express
@pytest.mark.parametrize(
    "minutes, bedding, express, expected",
    [
        # no bedding, not express -> cutoff 60, late 40..59
        (60, False, False, "accepted"),
        (59, False, False, "late"),
        (40, False, False, "late"),
        (39, False, False, "rejected"),
        # bedding, not express -> cutoff 90, late 70..89
        (90, True, False, "accepted"),
        (70, True, False, "late"),
        (69, True, False, "rejected"),
        # no bedding, express -> cutoff 90
        (90, False, True, "accepted"),
        (89, False, True, "late"),
        (69, False, True, "rejected"),
        # bedding + express -> cutoff 120, late 100..119
        (120, True, True, "accepted"),
        (100, True, True, "late"),
        (99, True, True, "rejected"),
    ],
)
def test_dropoff_status_all_branches(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected
