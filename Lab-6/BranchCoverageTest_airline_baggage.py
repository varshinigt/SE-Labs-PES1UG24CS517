import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ---- baggage_fee: validation ----
def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0

def test_exactly_at_allowance():
    assert baggage_fee("economy", 15, "domestic", False) == 0

def test_unknown_cabin():
    with pytest.raises(ValueError):
        baggage_fee("first", 10, "domestic", False)

def test_negative_weight():
    with pytest.raises(ValueError):
        baggage_fee("economy", -1, "domestic", False)

def test_zero_weight():
    assert baggage_fee("economy", 0, "domestic", False) == 0


# ---- baggage_fee: membership branches ----
def test_member_economy_gets_bonus():
    assert baggage_fee("economy", 25, "domestic", True) == 0       # allowance 25

def test_member_economy_over_bonus():
    assert baggage_fee("economy", 30, "domestic", True) == 100

def test_member_business_no_bonus():
    # allowance stays 40, excess 10 * 20
    assert baggage_fee("business", 50, "domestic", True) == 200

def test_nonmember_business():
    assert baggage_fee("business", 45, "domestic", False) == 100

def test_premium_nonmember_international():
    assert baggage_fee("premium", 30, "international", False) == 225


# ---- baggage_fee: route and excess branches ----
def test_domestic_light_excess():
    assert baggage_fee("economy", 25, "domestic", False) == 200

def test_international_light_excess():
    assert baggage_fee("economy", 25, "international", False) == 450

def test_domestic_excess_exactly_20():
    assert baggage_fee("economy", 35, "domestic", False) == 400    # not > 20

def test_domestic_heavy_excess():
    assert baggage_fee("economy", 40, "domestic", False) == 1000   # rate 40, no +10

def test_international_heavy_excess():
    assert baggage_fee("economy", 40, "international", False) == 2500


# ---- carry_on_ok ----
def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True

def test_carry_on_exactly_7kg():
    assert carry_on_ok(7, 1, False) is True

def test_carry_on_too_heavy():
    assert carry_on_ok(8, 1, False) is False

def test_carry_on_too_many_items():
    assert carry_on_ok(5, 2, False) is False

def test_infant_two_items():
    assert carry_on_ok(20, 2, True) is True

def test_infant_three_items():
    assert carry_on_ok(5, 3, True) is False


# ---- check_in_status (cutoffs: 60 / 45 domestic, 120 / 105 international) ----
@pytest.mark.parametrize("minutes, bag, intl, expected", [
    (60, True, False, "open"),   (45, True, False, "late"),   (44, True, False, "closed"),
    (45, False, False, "open"),  (30, False, False, "late"),  (29, False, False, "closed"),
    (120, True, True, "open"),   (105, True, True, "late"),   (104, True, True, "closed"),
    (105, False, True, "open"),  (90, False, True, "late"),   (89, False, True, "closed"),
])
def test_check_in_status(minutes, bag, intl, expected):
    assert check_in_status(minutes, bag, intl) == expected