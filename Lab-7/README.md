# Lab 7: Fuzzing for Input Validation Bugs (Airline Baggage Fees)

**Name:** Varshini A  **SRN:** PES1UG24CS517

**Forked repository:** https://github.com/varshinigt/L6_L7_28_airline_baggage/tree/main/lab7

Fuzz testing of `airline_baggage.py` (booking codes, bag weights, tag labels) using the Hypothesis library, followed by hardening of the code.

## Files

| File | Description |
|------|-------------|
| `airline_baggage.py` | Fixed (hardened) application script |
| `test_airline_baggage.py` | Hypothesis fuzz tests for all three functions |
| `REPORT.md` | Bugs found by fuzzing and how each was fixed |
| `Lab7_PES1UG24CS517.pdf` | Report with screenshots of every step |
| `screenshots/` | Terminal screenshots (install, buggy run, failing tests, fixed run, passing tests) |

## Run

```
pip install hypothesis pytest
python3 airline_baggage.py
python3 -m pytest test_airline_baggage.py
```

## Result

| Stage | Result |
|-------|--------|
| Original code, fuzz tests | 3 failed (2 distinct failures each) |
| Fixed code, fuzz tests | 3 passed |
