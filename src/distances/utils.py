from math import radians, cos, sin, asin, sqrt
import os
import pathlib
import platform

import pandas as pd

IS_WINDOWS = platform.system() == 'Windows'


class DistanceAPIError(Exception):
    pass


class DistanceIOError(Exception):
    pass


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


def validate_address(address):
    if 'DK' in address.upper():
        return address
    else:
        return f"{address}, DK"


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km
