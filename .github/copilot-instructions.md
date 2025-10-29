# Repository-wide Copilot Custom Instructions

This file provides custom instructions for GitHub Copilot and contributors. These guidelines apply to all requests and code contributions in this repository.

## Naming Standards
- Use descriptive, meaningful names for variables, functions, classes, and files.
- Follow snake_case for Python variables, functions, and file names (e.g., my_function, data_loader.py).
- Use PascalCase for class names (e.g., DataProcessor).
- Constants should be in ALL_CAPS (e.g., MAX_SIZE).
- Avoid abbreviations unless they are well-known and unambiguous.


## General Guidelines
- Follow PEP8 (for Python) or relevant language style guides.
- Write clear, concise, and well-documented code.
- Include type hints and docstrings for all public functions and classes.
- Add or update tests for any new features or bug fixes.
- Use descriptive commit messages (see example below).
- Open a pull request for all changes, referencing related issues if applicable.

## Commit Message Example
```
feat(module): add new data processing function

- Implemented process_data() in module.py
- Added unit tests for process_data()
- Updated README with usage example
```

## Example: Adding a New Function
1. Create your function in the appropriate module with docstrings and type hints.
2. Add tests in the corresponding test file.
3. Update documentation if needed.
4. Commit your changes with a descriptive message.
5. Open a pull request and fill out the checklist above.

---

