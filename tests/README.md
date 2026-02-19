# Space-API Tests

This directory contains all tests for the Space-API project.

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_unit.py` - Unit tests for individual components
- `test_integration.py` - Integration tests for API endpoints

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage
```bash
pytest --cov=src --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_unit.py
```

### Run specific test
```bash
pytest tests/test_unit.py::TestRootEndpoints::test_index_returns_404
```

### Run with verbose output
```bash
pytest -v
```

## Test Requirements

Tests require the following packages (included in requirements.txt):
- pytest
- pytest-cov

## Writing Tests

When writing new tests:
1. Create test functions prefixed with `test_`
2. Use descriptive test names that explain what is being tested
3. Follow the Arrange-Act-Assert pattern
4. Use fixtures from conftest.py for reusable setup

Example:
```python
def test_api_get_endpoint(client):
    """Test that /api/get returns value for valid path"""
    response = client.get('/api/get/state/open')
    assert response.status_code >= 200
    assert response.status_code < 300
```
