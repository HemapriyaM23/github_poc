# Contribution and Pull Request Instructions

To ensure code quality and consistency, all contributors and reviewers must follow these rules:

## Coding Standards
- **No DDL/DML with `DELETE *`:** Do not use `DELETE *` in any SQL statements. Use explicit column names and WHERE clauses.
- **Always use formatted strings:** Use f-strings (Python) or equivalent formatting in other languages. Avoid string concatenation for dynamic values.
- **Parameterize constants:** All constants must be defined and used as parameters. Avoid hardcoding values in code or queries.
- **Consistent library usage:** Use the same libraries for similar tasks throughout the codebase. Avoid mixing libraries for the same purpose.

## Pull Request Process
- All PRs must pass automated checks for the above rules.
- Copilot review is mandatory for every PR.
- Update or add tests for any new features or bug fixes.

---
