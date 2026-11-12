# Lab 7 Report: Fuzzing (Airline Baggage Fees)

**Name:** Varshini A  **SRN:** PES1UG24CS517

## Method
Each function was fuzzed with `@given(st.text() | st.none())`. The property tested: the function must not raise any exception for any string or `None`.

## Bugs found (original code)

| Function | Input found by Hypothesis | Exception | Cause |
|----------|---------------------------|-----------|-------|
| `parse_booking` | `''` | `ValueError: not enough values to unpack (expected 3, got 1)` | Unpacks `split('-')` without checking the number of parts |
| `parse_booking` | `None` | `AttributeError: 'NoneType' object has no attribute 'split'` | No type check |
| `total_weight` | `''` | `ValueError: could not convert string to float: ''` | Empty entry converted with `float()` unguarded |
| `total_weight` | `None` | `AttributeError` | No type check |
| `tag_label` | `''` | `IndexError: list index out of range` | Indexes `parts[0]` and `parts[1]` without checking length |
| `tag_label` | `None` | `AttributeError` | No type check |

Other weaknesses fixed in the same pass (not all shown by the fuzzer): non-numeric flight number, empty airline or seat, `nan`/`inf`/negative weights accepted as valid, and `tag_label` using the second word instead of the last word for names with a middle name.

## Fixes
- Added `isinstance(..., str)` checks in all three functions.
- `parse_booking`: require exactly 3 non-empty parts and an integer flight number.
- `total_weight`: wrap `float()` in `try/except`, reject `nan`, `inf` and negative values.
- `tag_label`: require at least first and last name; use the last word as surname.
- Invalid input now returns `None`, and `main()` prints a friendly message instead of crashing.

## Outcome
- Original code: 3 tests failed.
- Fixed code: 3 tests passed.
