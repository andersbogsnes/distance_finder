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
    try:
        return os.environ['API_KEY']
    except KeyError:
        message = f"""Must set API_KEY environment variable - type
        '{'set' if IS_WINDOWS else 'export'} API_KEY=<your-key>'
         at the terminal"""
        raise DistanceAPIError(message)


def read_data(file_path, column_name, **kwargs):
    file_path = pathlib.Path(file_path)

    if file_path.suffix == '.xlsx' or file_path.suffix == '.xls':
        df = pd.read_excel(file_path, **kwargs)

    elif file_path.suffix == '.csv':
        df = pd.read_csv(file_path, **kwargs)
    else:
        raise DistanceIOError(f"""{file_path.suffix} is unknown,
        use either excel or csv formats""")
    return df[column_name]


def validate_address(address):
    if 'DK' in address.upper():
        return address
    else:
        return f"{address}, DK"
