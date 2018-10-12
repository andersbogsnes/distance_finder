from distances.geocoding import get_lat_long


def test_get_lat_long_returns_expected_result(geocoding_response, monkeypatch):
    lat, lng = get_lat_long('Midtermolen 7, 2100')
    assert lat == 55.69808881
    assert lng == 12.59769149
