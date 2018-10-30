from typing import List

import requests
from .utils import DistanceAPIError
from .db import Address, Distance
from googlemaps import Client


def get_distance(from_address: 'Address', to_addresses: List['Address'], session, client: 'Client'):
    for to_address in to_addresses:
        distance = Distance.get_distance(session, from_address, to_address)
        if distance:
            yield distance
        else:
            distance_m, duration = call_google_api(from_address, to_address, client)
            yield Distance.create_distance(from_address=from_address,
                                           to_address=to_address,
                                           distance=distance_m,
                                           duration=duration,
                                           session=session)


def call_google_api(from_address: 'Address', to_address: 'Address', client: 'Client'):
    resp = client.distance_matrix([{"lat": from_address.lat,
                                    "lng": from_address.long
                                    }],
                                  [{"lat": to_address.lat,
                                    "lng": to_address.long}])
    if resp["status"] == "OK":
        base_resp = resp["rows"][0]["elements"][0]
        if base_resp["status"] == "OK":
            return base_resp["distance"]["value"], base_resp["duration"]["value"]

    raise DistanceAPIError(f"Issue with {from_address.address} or {to_address.address}")


def call_dawa(address):
    base_url = 'http://dawa.aws.dk/adresser'
    response = requests.get(base_url, params={"q": address, "struktur": "mini"})
    return response.json()


def get_lat_long(address):
    response = call_dawa(address)
    try:
        location = response[0]
    except IndexError:
        raise DistanceAPIError(f"{address} cannot be found - check for typos") from None
    return location["y"], location["x"]
