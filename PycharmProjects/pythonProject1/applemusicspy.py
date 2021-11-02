import requests
from typing import Any, Dict, List, Union

import pycountry
from urllib.parse import urlencode


def lookup(itunesID, trackName, albumArtist):
    url = "https://itunes.apple.com/lookup?id={}".format(itunesID)
    result = requests.get(url)

    try:
        json = result.json()['results']
        result_count = result.json()['resultCount']
    except KeyError:
        raise ConnectionError('Cannot fetch JSON data')

    if result_count == 0:
        url = 'https://itunes.apple.com/search?term={}'.format(trackName + "+" + albumArtist)
        result = requests.get(url)
        try:
            json = result.json()['results']
        except KeyError:
            raise ConnectionError('Cannot fetch JSON data')

    return json
