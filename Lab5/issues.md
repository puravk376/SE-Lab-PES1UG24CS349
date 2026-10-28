# Issues Found and Fixed: library_catalog_system.py

Before: Pylint 5.32/10, Bandit 5 issues (2 High, 1 Medium, 2 Low), Flake8 6 issues.
After: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| # | Issue | Type | Line(s) | Tool / Code | Severity | Description | Fix Approach |
|---|-------|------|---------|-------------|----------|-------------|--------------|
| 1 | Shell command injection | Security | 58 | Bandit B605 | High | `os.system("echo ... " + filename)` runs a shell with an unsanitised filename; a name like `x; rm -rf ~` would execute. | Removed `os.system`; print the message with `print()`. |
| 2 | Weak MD5 hash | Security | 47 | Bandit B324 | High | MD5 is broken and unsuitable for identifiers that need to be hard to forge. | Switched to `hashlib.sha256`. |
| 3 | Use of `eval` | Security | 42 | Bandit B307, Pylint W0123 | Medium | `eval(calc_expr)` executes arbitrary code passed in as a string. | Replaced with plain arithmetic: `days_overdue * rate_per_day`, with a `DAILY_FINE_RATE` constant. |
| 4 | Mutable default argument | Bug | 15 | Pylint W0102 | Medium | `active_issues=[]` is created once and shared across every call, so issue logs leak between calls. | Default to `None` and create a new list inside the function. |
| 5 | Bare `except: pass` | Bug / Security | 26-27 | Bandit B110, Pylint W0702, Flake8 E722 | Medium | Swallows every error (even `KeyboardInterrupt`) silently, so an unknown book id fails with no trace. | Catch `KeyError` only, log a warning, return `False`. |
| 6 | Hardcoded secret printed to console | Security | 62, 70 | Not flagged by any tool | High | `librarian_key` is a token committed in source and printed in plain text on every run. | Read it from the `LIBRARIAN_KEY` environment variable; print only whether it is configured. |
| 7 | Phantom return inflates stock | Logic bug | 23-27, 64 | Not flagged by any tool | Medium | `return_book("B02")` succeeds although B02 was never issued, raising stock from 1 to 2 copies. | Track a `total` per book; reject returns when `copies >= total`. |
| 8 | Insecure random PIN | Security | 51 | Bandit B311 | Low | `random` is predictable and unsuitable for PINs. | Use `secrets.randbelow`. |
| 9 | File not closed safely, no encoding | Quality | 55-57 | Pylint R1732, W1514 | Low | If `write` fails the file is never closed; encoding depends on the OS. | `with open(filename, "w", encoding="utf-8")`. |
| 10 | Unused import / variables | Style | 6, 31, 41 | Pylint W0611, W0612; Flake8 F401, F841 | Low | `csv`, `late_fee` and `days` are never used (`days` only existed for `eval`). | Removed them. |
| 11 | `== None` comparison and redundant if/else | Style | 32-37 | Pylint C0121, R1703, R1705; Flake8 E711 | Low | Non-idiomatic None check and an if/else that just returns a boolean. | `if book is None`, then `return book["copies"] > 0`. |
| 12 | Naming, docstrings, f-string, final newline | Style | 15, 19, all functions, 73 | Pylint C0103, C0116, C0209, C0304; Flake8 W292 | Low | camelCase `issueBook`, missing docstrings, `%` formatting, no newline at end. | Renamed to `issue_book`, added docstrings, used an f-string, added the newline. |
| 13 | `main()` runs on import | Quality | 73 | Not flagged | Low | Importing the module runs the demo and writes a file. | Wrapped in `if __name__ == "__main__":`. |
