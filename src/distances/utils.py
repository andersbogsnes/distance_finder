import os
import pathlib
import platform
import logging

import pandas as pd

from .db import Session, Address


IS_WINDOWS = platform.system() == 'Windows'

logger = logging.getLogger('distances.utils')


class DistanceAPIError(Exception):
    pass


class DistanceIOError(Exception):
    pass


def add_address(address: str, session: 'Session', home_office: bool) -> 'Address':
    logger.debug(f"Loading {address}")
    result = Address.get_address(session, address)
    if result:
        logger.debug(f"{address} found in DB")
        return result
    else:
        logger.debug(f"{address} not found in DB - Creating new address")
        return Address.create_address(session, address, home_office)


def get_api_key():
    api_key = os.getenv('API_KEY')
    if api_key is None:
        message = f"""Must set API_KEY environment variable
                      type '{'set' if IS_WINDOWS else 'export'} API_KEY=<your-key>' 
                      at the terminal"""
        raise DistanceAPIError(message)
    return api_key


def read_data(file_path: str, **kwargs) -> pd.DataFrame:
    file_path = pathlib.Path(file_path)

    if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
        df = pd.read_excel(file_path, **kwargs)

    elif file_path.suffix == '.csv':
        df = pd.read_csv(file_path, **kwargs)
    else:
        raise DistanceIOError(f"""{file_path.suffix} is unknown,
        use either excel or csv formats""")
    return df


def configure_logger():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_level = getattr(logging, log_level)
    base_logger = logging.getLogger('distances')
    base_logger.setLevel(log_level)

    default_handler = logging.StreamHandler()
    default_format = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s',
                                       datefmt='%H:%M:%S')
    default_handler.setFormatter(default_format)

    base_logger.addHandler(default_handler)
    return base_logger
