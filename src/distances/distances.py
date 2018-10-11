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
        self.from_addresses = self._load_data(file_path, from_column, office='office')
        self.to_addresses = self._load_data(file_path, to_column)

    def _load_data(self, file_path, column, office='office'):
        data = read_data(file_path, column)
        with self._session_scope() as session:
            addresses = [self._add_address(address, session) for address in data]
            session.add_all(addresses)
            session.commit()
            return [address.address for address in addresses]

    def _add_address(self, address, session):
        result = Address.address_exists(session, address)
        if result:
            return result
        else:
            lat, long = get_lat_long(self.client, address)
            new_address = Address(address=address, lat=lat, long=long)
            return new_address
