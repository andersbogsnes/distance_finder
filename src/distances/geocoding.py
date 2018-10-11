
def get_lat_long(client, address):
    response = client.geocode(address, components={'country': 'DK'})
    location = response[0]["geometry"]["location"]
    return location["lat"], location["lng"]
