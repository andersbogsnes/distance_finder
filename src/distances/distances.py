from googlemaps import Client
from .utils import get_api_key, read_data, validate_address
from .geocoding import get_xy_coordinates
from .db import Address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Distances:
    def __init__(self, connection_string=None):
        self.client = Client(get_api_key())
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def load_data(self, file_path, column):
        data = read_data(file_path, column)

        pass

    def add_address(self, address):
        session = self.Session()
        results = session.query(Address).where(Address.address == address).first()
        if results:
            return results
        else:
            lat, long = get_xy_coordinates(self.client, address)
            new_address = Address(address=address, lat=lat, long=long)

