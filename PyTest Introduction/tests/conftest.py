import pytest
import pandas as pd

# Fixture to read the CSV file
@pytest.fixture(scope='session')
def data(path_to_file):
    return pd.read_csv(path_to_file)

# Fixture to validate the schema of the file
@pytest.fixture(scope='session')
def validate_schema(actual_schema, expected_schema):
    errors = []

    missing = [col for col in expected_schema if col not in actual_schema]
    if missing:
        errors.append(f"Missing columns: {missing}")

    extra = [col for col in actual_schema if col not in expected_schema]
    if extra:
        errors.append(f"Extra columns: {extra}")

    for i, col in enumerate(expected_schema):
        if i < len(actual_schema) and actual_schema[i] != col:
            errors.append(f"Column order mismatch at position {i}: expected {col}, got {actual_schema[i]}")

    assert not errors, "\n".join(errors)


# Pytest hook to mark unmarked tests with a custom mark
def pytest_collection_modifyitems(items):
    for item in items:
        if not item.iter_markers():
            item.add_marker(pytest.mark.unmarked)
