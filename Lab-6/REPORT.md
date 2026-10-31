# Lab 6 Report: Code and Branch Coverage (Airline Baggage Fees)

Student: Varshini A (PES1UG24CS517)
Module under test: `airline_baggage.py` (`baggage_fee`, `carry_on_ok`, `check_in_status`)

## Tools
Python 3.13, pytest, coverage

## Commands used
```
pip install coverage pytest
coverage erase
coverage run -m pytest CodeCoverageTest_airline_baggage.py
coverage report -m
coverage erase
coverage run --branch -m pytest BranchCoverageTest_airline_baggage.py
coverage report -m
```

## Results
| Run | Test file | Tests | Statements | Missed | Branches | Partial | Coverage |
|---|---|---|---|---|---|---|---|
| Line coverage | CodeCoverageTest_airline_baggage.py | 11 passed | 37 | 0 | n/a | n/a | 100% |
| Branch coverage | BranchCoverageTest_airline_baggage.py | 33 passed | 37 | 0 | 26 | 0 | 100% |

The starter test file alone covered only 32% (line and branch), with most of the code untested.

## Analysis
**Line coverage.** 11 tests execute every statement: both `ValueError` paths, a member discount, the heavy-excess international rate, carry-on pass and fail, the infant rule, and all three check-in states (open, late, closed).

**Branch coverage.** Line coverage can hit every line without trying both outcomes of each decision. The branch test file adds the missing outcomes:
- Boundaries: weight exactly at the allowance, excess of exactly 20 kg (not above 20), carry-on of exactly 7 kg.
- Membership: the member bonus applies to economy and premium, but not business.
- Route and excess: domestic and international rates, each with light and heavy excess, including the extra +10 for heavy international excess only.
- Carry-on: too many items, infant with 2 items, infant with 3 items.
- Check-in: 12 parametrized cases at the cutoff and one minute before it, for baggage and no baggage, domestic and international.

All 26 branches were taken in both directions with no partially covered branches.

## Conclusion
Both targets (at least 90% code coverage and at least 90% branch coverage) were exceeded, reaching 100% on each.

## Files
- CodeCoverageTest_airline_baggage.py
- BranchCoverageTest_airline_baggage.py
- screenshots/code_coverage.png
- screenshots/branch_coverage.png
