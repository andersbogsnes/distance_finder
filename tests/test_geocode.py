from distances.geocoding import get_lat_long


def test_get_lat_long_returns_expected_result(geocoding_response, client):
    lat, lng = get_lat_long(client, 'test_address')
    assert lat == 39.8628316
    assert lng == -4.027323099999999
