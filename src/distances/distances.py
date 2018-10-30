from typing import List

from googlemaps import Client

from .geocoding import get_distance
from .utils import get_api_key, read_data, DistanceIOError, configure_logger, add_address
from .db import Address, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

logger = configure_logger()


class Distances:
    def __init__(self, connection_string=None):
        self.client = Client(get_api_key())
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.from_addresses = []
        self.to_addresses = []
        self.results = []
        Base.metadata.create_all(bind=self.engine)

    def import_data_from_df(self, df, from_column=None, to_column=None):
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

        addresses = [add_address(address, self.session, home_office)
                     for address
                     in data]
        return addresses

    def get_distances(self):
        for index, office in enumerate(self.from_addresses, start=1):
            logger.info(
                f"{index}/{len(self.from_addresses)}: Calculating distance from {office.address}")
            for distance in get_distance(office, self.to_addresses,
                                         client=self.client,
                                         session=self.session):
                self.results.append(distance)
        return self.results

    def output_distances(self):
        if not self.results:
            self.get_distances()

        data = [(distance.from_address.address,
                 distance.to_address.address,
                 distance.duration,
                 distance.distance) for distance in self.results]

        return pd.DataFrame(data=data, columns=['from_address',
                                                'to_address',
                                                'duration',
                                                'distance'])
