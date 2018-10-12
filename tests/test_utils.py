import pytest
import os
import pandas as pd

from distances.utils import get_api_key, DistanceAPIError, read_data, validate_address


def test_get_api_key_works_as_expected_with_key_set():
    # ENV is set
    os.environ["API_KEY"] = '1234'
    result = get_api_key()

    assert '1234' == result

    # ENV is unset
    del os.environ["API_KEY"]
    with pytest.raises(DistanceAPIError,
                       match="Must set API_KEY environment variable"):
        get_api_key()


def test_read_data_works_with_excel(excel_file, dummy_df):
    col_name = dummy_df.columns[0]
    df = read_data(excel_file)[col_name]
    assert set(dummy_df[col_name]) == set(df)
    assert isinstance(df, pd.Series)


def test_read_data_works_with_csv(csv_file, dummy_df):
    col_name = dummy_df.columns[0]
    df = read_data(csv_file)[col_name]
    assert set(dummy_df[col_name]) == set(df)
    assert isinstance(df, pd.Series)


@pytest.mark.parametrize('address, expected', [
    ('Husmarkvej 12b, 2720, DK', 'Husmarkvej 12b, 2720, DK'),
    ('Testgade', 'Testgade, DK'),
    ('12 Testevej 5000', '12 Testevej 5000, DK'),
    ('40 Hogwarts, dk', '40 Hogwarts, dk')
])
def test_validate_address(address, expected):
    result = validate_address(address)
    assert expected == result
