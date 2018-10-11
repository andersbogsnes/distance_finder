import os
import platform

IS_WINDOWS = platform.system() == 'Windows'


class APIError(Exception):
    pass


def get_api_key():
    try:
        return os.environ['API_KEY']
    except KeyError:
        message = f"""Must set API_KEY environment variable - 
        use {'set' if IS_WINDOWS else 'export'} API_KEY=<your-key>' at the terminal"""
        raise APIError(message)