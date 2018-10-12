from typing import List

from googlemaps import Client

from .geocoding import calculate_distances
from .utils import get_api_key, read_data, DistanceIOError
from .db import Address, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd


class Distances:
    def __init__(self, connection_string=None):
        self.client = Client(get_api_key())
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.from_addresses = []
        self.to_addresses = []
        self.results = {}
        Base.metadata.create_all(bind=self.engine)

    def import_data_from_df(self, df, from_column, to_column):
        if to_column is None and from_column is None:
            raise DistanceIOError("""Must specify one of
            'from_column' or 'to_column'""")

        if from_column:
            self.from_addresses = self._load_data(df[from_column], home_office=False)

        if to_column:
            self.to_addresses = self._load_data(df[to_column], home_office=True)

        return self

    def import_data_from_file(self,
                              file_path: str,
                              from_column: str = 'from_address',
                              to_column: str = 'to_address') -> 'Distances':
        """
        Import data from file - specify from addresses and to addresses
        :param file_path:
            path to input file
        :param from_column:
            name of column
        :param to_column:
            name of column
        :return:
            returns self
        """

        df = read_data(file_path)

        self.import_data_from_df(df, from_column, to_column)

        return self

    def _load_data(self, data: pd.DataFrame, home_office: bool) -> List[Address]:
        """
        Internal helper for loading data - checks if each address exists in the database
        adds them if not present.
        :param data: Dataframe of input data
        :param home_office: boolean whether or not this address is a homeoffice
        :return:
        """

        addresses = [self._add_address(address, self.session, home_office) for address in data]
        return addresses

    def _add_address(self, address: str, session: 'Session', home_office: bool) -> 'Address':
        result = Address.get_address(session, address)
        if result:
            return result
        else:
            return Address.create_address(session, address, home_office)

    def get_distances(self):
        for office in self.from_addresses:
            self.results[office.address] = calculate_distances(office,
                                                               self.to_addresses,
                                                               self.client,
                                                               self.session)

        return self.results
