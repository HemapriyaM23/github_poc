
---
applyTo: "test/**/*.py"
---

# Path-Specific Copilot Custom Instructions for test/

These instructions apply only to files within the `test/` directory.

## Testing Standards
- All test files must be named with the prefix `test_` (e.g., `test_example.py`).
- Use pytest for writing and running tests.
- Each test function should start with `test_` and include a descriptive name.
- Use descriptive assertions and avoid bare `assert` statements when possible.
- Mock external dependencies to ensure tests are isolated.
- Include docstrings for complex test cases.

## Example: Writing a Test
```python
# test/test_module.py

def test_addition():
    """Test that addition works correctly."""
    result = 2 + 3
    assert result == 5
```

---

For more details, refer to the repository-wide instructions or contact the maintainer.
