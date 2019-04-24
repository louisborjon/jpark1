import __future__
import os, sys, json

from urllib.request import urlopen as urlopen
from urllib.parse import quote_plus as quote_plus

def geocode(mapbox_access_token, query):
    """
    Submit a geocoding query to Mapbox's geocoder.
    Args:
        mapbox_access_token (str): valid Mapbox access token with geocoding permissions
        query (str): input text to geocode
    """
    resp = urlopen('https://api.tiles.mapbox.com/geocoding/v5/mapbox.places/{query}.json?access_token={token}'.format(query=quote_plus(query), token=mapbox_access_token))
    results = json.loads(resp.read().decode('utf-8'))
    return results["features"][0]["center"]

if __name__ == '__main__':
    token = "sk.eyJ1Ijoidml0aHV5YW4iLCJhIjoiY2p1dWI0b2ZtMDVkeDN5bXF5dmR5NWlzNyJ9.XytADzlzPvLuSXPI5vroJw"

    # geocode
    result = geocode(token, "100 king street west, toronto")

    # print result
    print(json.dumps(result, indent=2))
