
# CONTRIBUTING GUIDELINES

All contributors and reviewers (including Copilot) must follow these rules for every code change and pull request:

## Coding Standards (MANDATORY)

1. **No usage of `DELETE *` in SQL statements**
	- Never use `DELETE *` in any SQL query.
	- Always specify columns and use a WHERE clause to avoid accidental data loss.

2. **All dynamic strings must use formatted strings**
	- In Python, always use f-strings (e.g., `f"Hello, {name}"`).
	- Do not use string concatenation or `%` formatting for dynamic values.

3. **All constants should be parameterized, not hardcoded**
	- Define constants at the top of the file or in a config file.
	- Do not hardcode values directly in code or queries.

4. **Consistent usage of libraries throughout the codebase**
	- Use the same library for the same purpose everywhere (e.g., use only `requests` for HTTP calls, not a mix of `requests` and `urllib`).

## Pull Request Review Checklist

For every PR, Copilot and human reviewers must:

- [ ] Check for any use of `DELETE *` in SQL and request changes if found.
- [ ] Ensure all dynamic strings use formatted strings (f-strings in Python).
- [ ] Verify all constants are parameterized and not hardcoded.
- [ ] Confirm consistent library usage for similar tasks.
- [ ] Leave specific review comments for any violations, referencing the rule above.
- [ ] Approve the PR only if all rules are followed.

---
