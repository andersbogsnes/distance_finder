from typing import List

import requests
from .db import Distance, Address
from .utils import DistanceAPIError
from googlemaps import Client


def get_distance(from_address: 'Address', to_addresses: List['Address'], session, client: 'Client'):
    for to_address in to_addresses:
        distance = Distance.get_distance(session, from_address, to_address)
        if distance:
            yield to_address, distance
        else:
            distance_m, duration = fetch_distance(from_address, to_address, client)
            yield to_address, Distance.create_distance(from_address=from_address,
                                                       to_address=to_address,
                                                       distance=distance_m,
                                                       duration=duration,
                                                       session=session)


def fetch_distance(from_address: 'Address', to_address: 'Address', client: 'Client'):
    resp = client.distance_matrix([{"lat": from_address.lat,
                                    "long": from_address.long
                                    }],
                                  [{"lat": to_address.lat,
                                    "long": to_address.long}])
    base_resp = resp["rows"][0]["elements"]
    if base_resp["status"] == "OK":
        return base_resp["distance"], base_resp["duration"]
    else:
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
        raise DistanceAPIError(f"{address} cannot be found - check for typos")
    return location["y"], location["x"]


def calculate_distances(office, to_addresses, client, session, max_haversine=50):
    filtered_to_addresses = [address
                             for address
                             in to_addresses
                             if office.haversine(address) > max_haversine]

    return [(office, to_address, distance)
            for to_address, distance
            in get_distance(office,
                            filtered_to_addresses,
                            client=client,
                            session=session)]
