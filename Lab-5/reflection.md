# Lab 5 Reflection: Static Code Analysis (blood_donation.py)

> **Note:** The four reflection questions mentioned in the README were not included in the lab handout provided to me. The questions below are my own, covering what the lab is meant to teach (what I found, what was hard, what the tools got wrong, and how I would use them in future). 

## 1. What did static analysis find that I would probably have missed by just running the program?

The program ran fine and printed sensible output, yet the three tools found 4 Bandit issues, 28 Pylint messages (score 4.81/10) and 4 Flake8 warnings. The most important ones never show up in a demo run:

- `os.system("send-sms " + " ".join(phoneList))` allows command injection, but only if someone passes a malicious phone number. The demo never calls this function.
- `tempfile.mktemp` has a race condition that only matters if an attacker is watching the temp folder.
- `notes=[]` is a mutable default argument. The same list is shared across every call, so it only misbehaves when the function is called more than once with the default.
- `except Exception` hid errors. It would swallow any bug inside `units_for`, not just an unknown blood group.

Static analysis reads the code itself, so it finds problems in code paths that a short demonstration never runs.

## 2. Which issues were easiest and hardest to fix?

**Easiest:** the Flake8 formatting problems (`eligible=` to `eligible = `, two spaces before `#`, the extra blank line, the long line) and the Pylint docstring and naming messages. The reports said exactly what to change, and none of it affected behaviour.

**Hardest:** the security issues, because I had to understand why they are dangerous before fixing them properly.
- Replacing `os.system` meant learning that passing a list to `subprocess.run` (with no shell) stops the input being interpreted as shell commands.
- Replacing `mktemp` with `NamedTemporaryFile` meant understanding that creating the file and choosing its name must happen in one step.
- The mutable default argument was hard to spot because the code looks correct.

## 3. Did the tools produce warnings that were not real problems?

Yes. After replacing `os.system` with `subprocess.run`, Bandit raised low-severity warnings about importing and calling `subprocess` (B404, B603, B607). These are informational. The call uses a fixed command name with arguments as a list and no shell, so it is not injectable. I suppressed those three with `# nosec` comments after checking this. Bandit reported 0 issues and listed 3 suppressed ones.

This showed me that a tool report is a list of things to review, not an automatic verdict. A human still has to decide whether each warning is real, and suppressions should be rare and deliberate.

I also made a small mistake myself: after pasting my fixed file I added an extra blank line at the end, and Flake8 (W391) and Pylint (C0305) flagged it, dropping Pylint to 9.84. Rerunning the tools caught it and I fixed it. This is a good example of why the lab says to rerun the tools until the reports are clean.

## 4. What improved, and how would I use these tools in future?

| Tool | Before | After |
|------|--------|-------|
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | 0 issues |
| Pylint | 4.81/10 | 10.00/10 |
| Flake8 | 4 warnings | 0 warnings |

The program prints exactly the same output as before, so the fixes did not change behaviour.

- **Security:** no command injection, no predictable temp file, no hardcoded password, and validation that cannot be removed by running Python with `-O`.
- **Reliability:** no data shared between calls, and errors are no longer hidden by a broad `except`.
- **Readability:** PEP 8 names, docstrings, named constants (`MIN_AGE`, `MAX_AGE`, `DONATION_GAP_DAYS`) and consistent formatting make the code easier to read and maintain.

In future projects I would run Flake8, Pylint and Bandit automatically before each commit (for example with a pre-commit hook) and again in a CI pipeline, so problems are caught while the code is fresh and before anyone reviews it. Static analysis does not replace testing or code review, but it catches a whole class of mistakes cheaply and consistently.
