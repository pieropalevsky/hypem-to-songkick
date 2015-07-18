from urllib.parse import urlencode
from collections import Counter, OrderedDict
import re

import requests

import app.constants as c


def get_songkick_url(artist):
    return "https://www.songkick.com/search?page=1&per_page=10&" + urlencode({'query': artist}) + "&type=artists"


def add_songkick_url(dictionary):
    for artist, info in dictionary.items():
        info['songkick_url'] = get_songkick_url(artist)


def get_hypem_artists(username):
    """
    Returns an ordered dictionary { 'artist_name': {'count: int, 'songkick_url': str}
    """
    artist_list = []
    cleaned_artist_list = []
    artists_od = OrderedDict()

    """
    Makes calls to hypem in json and adds artists until there is a timeout on
    the paging
    """
    i = 1
    page = requests.get('http://hypem.com/playlist/loved/' + username + '/json/' + str(i) + '/data.js', timeout=1)
    while page.status_code == 200:
        data = page.json()
        data.pop("version", None)
        for key in data:
            artist_list.append(data[key]['artist'].lower())
        i += 1
        page = requests.get('http://hypem.com/playlist/loved/' + username + '/json/' + str(i) + '/data.js')

    """
    Artist name processing to deal with remixes, collaborations and featured
    artists
    """
    for artist in set(artist_list):
        if artist.strip() != '':
            for contributor in re.split("|".join(c.delimiters), artist):
                cleaned_artist_list.append(contributor.strip())

    """
    Adds the artists name, number of favorites and the songkick url the
    ordered dictionary to be returned
    """
    for a in Counter(cleaned_artist_list).most_common():
        artists_od[a[0]] = {'count': a[1]}
    add_songkick_url(artists_od)

    return artists_od
