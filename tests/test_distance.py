from distances.db import Address
import pandas as pd


def test_db_connection(distance):
    conn = distance.engine.connect()
    res = conn.execute("SELECT * FROM address").fetchall()
    assert [] == res


def test_add_address(geocoding_response, distance):
    test_address = 'Midtermolen 7, 2100'
    with distance._session_scope() as session:
        distance._add_address(test_address, session)


def test_Address_exists(distance):
    new_address = Address(address="test")
    with distance._session_scope() as session:
        session.add(new_address)

    with distance._session_scope() as session:
        assert Address.address_exists(session, "test")


def test_load_data(excel_file, distance):
    distance._load_data(excel_file, 'from_address')
    df = pd.read_excel(excel_file)['from_address']
    with distance._session_scope() as session:
        for address in df.unique():
            assert Address.address_exists(session, address)


def test_import_data(excel_file, distance):
    distance.import_data(file_path=excel_file)
    with distance._session_scope() as session:
        for address in distance.from_addresses:
            assert Address.address_exists(session, address)

        for address in distance.to_addresses:
            assert Address.address_exists(session, address)
