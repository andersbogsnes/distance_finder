from distances.db import Address
import pandas as pd


def test_db_connection(distance):
    conn = distance.engine.connect()
    res = conn.execute("SELECT * FROM address").fetchall()
    assert [] == res


def test_add_address(geocoding_response, distance, session):
    test_address = 'Midtermolen 7, 2100'
    distance._add_address(test_address, session, home_office=False)


def test_Address_exists(session):
    new_address = Address(address='test', home_office=True)
    session.add(new_address)
    session.commit()
    assert Address.get_address(session, "test")


def test_load_data(excel_file, distance):
    df = pd.read_excel(excel_file)['from_address']
    distance._load_data(df, home_office=False)

    for address in df.unique():
        assert Address.get_address(distance.session, address)


def test_import_data(excel_file, distance):
    distance.import_data_from_file(file_path=excel_file)
    for address in distance.from_addresses:
        assert Address.get_address(distance.session, address.address)

    for address in distance.to_addresses:
        assert Address.get_address(distance.session, address.address)
