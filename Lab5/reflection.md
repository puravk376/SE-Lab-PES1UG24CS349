# Reflection: Static Code Analysis

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the style issues from Flake8 and Pylint: the unused `csv` import, `== None`, the missing final newline, the camelCase name and the missing docstrings. Each one had a single obvious fix and no effect on behaviour. The hardest was `eval()` in `calculate_fine`, because removing it changed the function's interface: the caller passed a formula string, so I had to decide what the function should actually accept (a day count and a rate) and update `main()` to match. The phantom-return bug in `return_book` was also hard because no tool reported it; I only noticed it by reading the output and the code, and fixing it meant adding a `total` field to each catalog entry.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Yes. Pylint and Flake8 both reported `days` in `calculate_fine` as an unused variable, but it was used: `eval("days * 2.0")` read it by name at runtime. A static tool cannot see inside a string being evaluated, so the warning was technically wrong. It still pointed at a real problem, though, because code that only works through `eval` is fragile and unsafe. Bandit's B311 warning on `random` is also a near false positive in many programs (for example shuffling a list), but here it was valid because the number is a PIN.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would run them in two places. Locally, as a pre-commit hook (using the `pre-commit` framework) so Flake8 and Bandit run on every commit and block it on new errors. In CI, as a GitHub Actions job that runs Pylint, Flake8 and Bandit on every push and pull request, fails the build on any Bandit High/Medium finding or a Pylint score under 9.5, and uploads the reports as artifacts. Project-wide settings would go in `.pylintrc`, `.flake8` and `pyproject.toml` so everyone uses the same rules, and editor plugins would show warnings while typing.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The Pylint score went from 5.32 to 10.00, Bandit went from 5 issues (2 High) to 0, and Flake8 went from 6 issues to 0. In practice: the code can no longer run arbitrary shell commands or Python expressions, the hash is no longer MD5, and the librarian key is no longer stored in or printed from the source. Errors are no longer swallowed silently; an unknown book id now logs a warning and returns `False`. Stock counts stay correct because a book that was never issued cannot be returned. Every function has a docstring and a consistent name, and the module can be imported without side effects, which makes it easier to test.
