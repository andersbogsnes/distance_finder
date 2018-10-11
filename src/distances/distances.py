from googlemaps import Client
from .utils import get_api_key


class Distances:
    def __init__(self):
        self.client = Client(get_api_key())
