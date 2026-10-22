# Issues Found: Lab 5 Static Code Analysis (blood_donation.py)

Line numbers refer to the original file (see `*_before.txt` reports).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `os.system` with a string built from input (Bandit B605) | Security (High) | 65 | The shell command is built by joining phone numbers into a string, so crafted input could run arbitrary commands (command injection). | Replaced with `subprocess.run(["send-sms", *phone_list])`, passing a list with no shell. |
| `tempfile.mktemp` (Bandit B306) | Security (Medium) | 60 | `mktemp` returns a predictable file name without creating the file, which causes a race condition. | Replaced with `tempfile.NamedTemporaryFile(suffix=".csv", delete=False)`. |
| Hardcoded password `OFFICER_PASSWORD` (Bandit B105) | Security (Low) | 5 | A password stored in source code can leak through the repo. | Removed it, since it was never used. |
| `assert` used for validation (Bandit B101) | Security (Low) | 18 | Asserts are removed when Python runs with `-O`, so the blood group check could silently disappear. | Replaced with `if ... : raise ValueError("Unknown blood group")`. |
| Mutable default argument `notes=[]` (Pylint W0102) | Bug | 17 | The same list is shared across every call, so data leaks between calls. | Default is now `None`, and a new list is created inside the function. |
| Overly broad `except Exception` (Pylint W0718) | Bug | 45 | Catches every error and hides real bugs. | Now catches only `KeyError`, which is what an unknown blood group raises. |
| Repeated comparisons (Pylint R1714) | Refactor | 50 | `x == "O-" or x == "AB+"` is clumsy. | Changed to `blood_group in ("O-", "AB+")`. |
| camelCase names (Pylint C0103) | Style | 17, 27, 33, 42, 49, 53, 58, 63 | Function and argument names do not follow PEP 8 snake_case. | Renamed, e.g. `registerDonor` to `register_donor`, `donorName` to `donor_name`. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1 and every function | No module or function documentation. | Added a module docstring and a docstring for every function. |
| Missing `main` guard | Style | last line | `main()` ran on import. | Wrapped in `if __name__ == "__main__":`. |
| Line too long, 82 > 79 (Flake8 E501) | Style | 7 | Exceeds the PEP 8 line length. | Split the `stock` dictionary over two lines. |
| Too many blank lines (Flake8 E303) | Style | 58 | Three blank lines before a function instead of two. | Removed the extra blank line. |
| One space before inline comment (Flake8 E261) | Style | 80 | Needs at least two spaces before `#`. | Added a second space. |
| Missing whitespace around `=` (Flake8 E225) | Style | 81 | `eligible=[...]` is not PEP 8. | Changed to `eligible = [...]`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Pylint | 4.81/10 | 10.00/10 |
| Flake8 | 4 warnings | 0 warnings |