import pytest
import pandas as pd


@pytest.fixture
def dummy_df():
    return pd.DataFrame({"col1": [1, 2, 3, 4], "col2": [5, 6, 7, 8]})


@pytest.fixture
def excel_file(tmpdir, dummy_df):
    file_name = tmpdir.join('test.xlsx')
    dummy_df.to_excel(file_name)
    return file_name


@pytest.fixture
def csv_file(tmpdir, dummy_df):
    file_name = tmpdir.join('test.csv')
    dummy_df.to_csv(file_name)
    return file_name
