from googlemaps import Client
from .utils import get_api_key, read_data
from .geocoding import get_lat_long
from .db import Address, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.exc import DatabaseError


class Distances:
    def __init__(self, connection_string=None):
        self.client = Client(get_api_key())
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.from_addresses = None
        self.to_addresses = None
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def _session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except DatabaseError:
            session.rollback()
        finally:
            session.close()

    def import_data(self, file_path, from_column='from_address', to_column='to_address'):
        self.from_addresses = self._load_data(file_path, from_column, home_office=False)
        self.to_addresses = self._load_data(file_path, to_column, home_office=True)

    def _load_data(self, file_path: str, column: str, home_office: bool):
        data = read_data(file_path, column)
        with self._session_scope() as session:
            addresses = [self._add_address(address, session, home_office) for address in data]
            session.add_all(addresses)
            session.commit()
            return [address.address for address in addresses]

    def _add_address(self, address, session, home_office):
        result = Address.get_address(session, address)
        if result:
            return result
        else:
            return Address.create_address(self.client, session, address, home_office)
