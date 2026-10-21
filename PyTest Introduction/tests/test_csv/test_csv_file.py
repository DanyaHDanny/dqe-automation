import pytest

def test_file_not_empty(csv_data):
    assert len(csv_data.index) > 0, f"The file {csv_data.filename} is empty."

@pytest.mark.validate_csv
@pytest.mark.xfail(reason="Known bug")
def test_duplicates(csv_data):
    duplicate_rows = csv_data[csv_data.duplicated()]
    assert duplicate_rows.empty, f"Found duplicate rows:\n{duplicate_rows}"

@pytest.mark.validate_csv
def test_validate_schema(csv_data, validate_schema):
    expected_schema = {
        "id": "int64",
        "name": "object",
        "age": "int64",
        "email": "object",
        "is_active": "bool"
    }

    # Extract the actual schema
    actual_schema = {col: str(csv_data[col].dtype) for col in csv_data.columns}

    # Use the schema validation utility
    validation_result = validate_schema(actual_schema, expected_schema)

    assert validation_result["is_valid"], f"Schema validation failed! Errors: {validation_result['errors']}"

@pytest.mark.validate_csv
@pytest.mark.skip(reason="Skipping this test for demonstration")
def test_age_column_valid(csv_data):
    invalid_ages = csv_data['age'][~csv_data['age'].apply(lambda x: 0 <= x <= 100)]
    assert invalid_ages.empty, f"Invalid ages found: {invalid_ages.tolist()}"

@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    invalid_emails = csv_data['email'][~csv_data['email'].str.match(email_regex, na=False)]
    assert invalid_emails.empty, f"Invalid email addresses found: {invalid_emails.tolist()}"

@pytest.mark.parametrize("id, is_active", [[1, False], [2, True]])
def test_active_players(csv_data, id, is_active):
    # Get the row corresponding to the given ID
    player_row = csv_data[csv_data['id'] == id]

    # Assert that the 'is_active' value matches the expected value
    actual_is_active = player_row['is_active'].iloc[0]
    assert actual_is_active == is_active, f"Player with ID {id} has incorrect 'is_active' value. Expected: {is_active}, Got: {actual_is_active}"

def test_active_player(csv_data):
    assert csv_data.loc[csv_data['id'] == 2, 'is_active'].values[0] == True, f"Player with 2 ID has incorrect 'is_active' value."
