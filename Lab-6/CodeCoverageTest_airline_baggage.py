import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ---- baggage_fee ----
def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0

def test_unknown_cabin():
    with pytest.raises(ValueError):
        baggage_fee("first", 10, "domestic", False)

def test_negative_weight():
    with pytest.raises(ValueError):
        baggage_fee("economy", -1, "domestic", False)

def test_member_domestic_small_excess():
    # allowance 15+10=25, excess 5, rate 20
    assert baggage_fee("economy", 30, "domestic", True) == 100

def test_international_heavy_excess():
    # excess 25, rate (45*2)+10 = 100
    assert baggage_fee("economy", 40, "international", False) == 2500


# ---- carry_on_ok ----
def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True

def test_carry_on_too_heavy():
    assert carry_on_ok(8, 1, False) is False

def test_carry_on_infant():
    assert carry_on_ok(5, 2, True) is True


# ---- check_in_status ----
def test_status_open():
    assert check_in_status(120, True, True) == "open"

def test_status_late():
    assert check_in_status(30, False, False) == "late"

def test_status_closed():
    assert check_in_status(10, True, False) == "closed"