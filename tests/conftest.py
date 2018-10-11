import pytest
import pandas as pd
from distances import Distances
import os
import json
import googlemaps


@pytest.fixture
def dummy_df():
    return pd.DataFrame({"from_address": ["Midtermolen 7, 2100",
                                          "Bogholder Allé 29A, 2720",
                                          "Rådhuspladsen 2-4, 1550"],
                         "to_address": ["Halmtorvet 29C, 1700",
                                        "Linnésgade 16D, 1361",
                                        "Borgergade 93, 1300"]})


@pytest.fixture(autouse=True)
def patch_geocode(monkeypatch, geocoding_response):
    def mock_response(*args, **kwargs):
        return geocoding_response["results"]

    monkeypatch.setattr('googlemaps.Client.geocode', mock_response)


@pytest.fixture
def distance():
    os.environ['API_KEY'] = 'AIzaasdf'
    return Distances('sqlite:///:memory:')


@pytest.fixture
def client():
    return googlemaps.Client('AIzaasdf')


@pytest.fixture
def excel_file(tmpdir, dummy_df):
    file_name = tmpdir.join('test.xlsx')
    dummy_df.to_excel(file_name)
    return file_name


@pytest.fixture
def csv_file(tmpdir, dummy_df):
    file_name = tmpdir.join('test.csv')
    dummy_df.to_csv(file_name)
    return file_name


@pytest.fixture
def geocoding_response():
    return {
        "results": [
            {
                "address_components": [
                    {
                        "long_name": "Toledo",
                        "short_name": "Toledo",
                        "types": ["locality", "political"]
                    },
                    {
                        "long_name": "Toledo",
                        "short_name": "TO",
                        "types": ["administrative_area_level_2", "political"]
                    },
                    {
                        "long_name": "Castile-La Mancha",
                        "short_name": "CM",
                        "types": ["administrative_area_level_1", "political"]
                    },
                    {
                        "long_name": "Spain",
                        "short_name": "ES",
                        "types": ["country", "political"]
                    }
                ],
                "formatted_address": "Toledo, Spain",
                "geometry": {
                    "bounds": {
                        "northeast": {
                            "lat": 39.88605099999999,
                            "lng": -3.9192423
                        },
                        "southwest": {
                            "lat": 39.8383676,
                            "lng": -4.0796176
                        }
                    },
                    "location": {
                        "lat": 39.8628316,
                        "lng": -4.027323099999999
                    },
                    "location_type": "APPROXIMATE",
                    "viewport": {
                        "northeast": {
                            "lat": 39.88605099999999,
                            "lng": -3.9192423
                        },
                        "southwest": {
                            "lat": 39.8383676,
                            "lng": -4.0796176
                        }
                    }
                },
                "place_id": "ChIJ8f21C60Lag0R_q11auhbf8Y",
                "types": ["locality", "political"]
            }
        ],
        "status": "OK"
    }
