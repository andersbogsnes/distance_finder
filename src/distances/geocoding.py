def get_xy_coordinates(client, address):
    return client.geocoding(address, components={'country': 'DK'})
