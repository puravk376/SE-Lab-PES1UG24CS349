"""
Lab 6 - Code (Line) Coverage Tests
Name : Purav N Khincha
SRN  : PES1UG24CS349
Repo : L6_L7_41_laundry_service

Goal: execute every statement in laundry_service.py at least once
(>= 90% line coverage).
"""
import pytest
from laundry_service import extra_weight_charge, order_acceptable, dropoff_status


# ---------------- starter tests (given) ----------------
def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_order_acceptable():
    assert order_acceptable(10, 20, False) is True


# ---------------- extra_weight_charge ----------------
def test_unknown_garment_type_raises():
    with pytest.raises(ValueError, match="unknown garment type"):
        extra_weight_charge("silk", 5, "standard", False)


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_gets_two_extra_kg_standard_rate():
    # regular: 5 + 2 (member) = 7 included -> extra 3 kg * 30
    assert extra_weight_charge("regular", 10, "standard", True) == 90


def test_non_standard_speed_rate():
    # delicate: 3 included -> extra 2 kg * 50
    assert extra_weight_charge("delicate", 5, "express", False) == 100


def test_heavy_express_surcharge():
    # regular: 5 included -> extra 15 kg, rate 50 + 15 + 10 = 75
    assert extra_weight_charge("regular", 20, "express", False) == 1125


# ---------------- order_acceptable ----------------
def test_delicate_order_items_limit():
    assert order_acceptable(5, 3, True) is True


def test_order_too_heavy():
    assert order_acceptable(30, 10, False) is False


# ---------------- dropoff_status ----------------
def test_dropoff_bedding_accepted():
    # cutoff 90
    assert dropoff_status(100, True, False) == "accepted"


def test_dropoff_express_late():
    # cutoff 60 + 30 = 90 -> late window 70..89
    assert dropoff_status(75, False, True) == "late"


def test_dropoff_rejected():
    # cutoff 60 -> anything below 40 rejected
    assert dropoff_status(10, False, False) == "rejected"
