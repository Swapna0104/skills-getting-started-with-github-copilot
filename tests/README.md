# Tests

This directory contains tests for the FastAPI backend application.

## Running Tests

To run the tests, make sure you have the dependencies installed:

```bash
pip install -r requirements.txt
```

Then run the tests with pytest:

```bash
pytest tests/
```

## Test Coverage

The tests cover the following API endpoints:

- `GET /activities` - Retrieve all activities
- `POST /activities/{activity_name}/signup` - Sign up for an activity
- `DELETE /activities/{activity_name}/signup` - Unregister from an activity
- `GET /` - Root redirect to static index

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_api.py` - API endpoint tests with comprehensive coverage of success and error cases