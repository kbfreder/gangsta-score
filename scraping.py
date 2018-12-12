import requests
from bs4 import BeautifulSoup
import re
import json
import util as u
import datetime as dt

artist_splitter = re.compile(r'( Featuring | X |, | & )')
song_splitter = re.compile('( \()')
token = 'HTVFOfb4OTB04zvV4zfmtv8Oeu5cKecEHRA_aw4gi6-4KC2kaaszNQ6yIQxLGera'

def search_song_artist(song_title, artist_name):
    base_url = 'https://api.genius.com'
    # the latter part is my Client Access Token
    headers = {'Authorization': 'Bearer ' + token}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response


def get_song_url(response, artist):
    json = response.json()
    song_match = None
    for hit in json['response']['hits']:
        if artist.lower() in hit['result']['primary_artist']['name'].lower():
            song_match = hit
            break
    try:
        song_url = song_match['result']['url']
    except TypeError:
        err_timestamp = dt.datetime.now()
        u.log_this(f'{err_timestamp:%Y-%m-%d %H:%M} - get_song_url error: {artist}, {response.url}')
        song_url = None
    return song_url


def scrape_song_url(url):
    try:
        page = requests.get(url)
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics = html.find('div', class_='lyrics').get_text()
    except AttributeError:
        lyrics = "error"
    try:
        album = html.find('span', string='Album').find_all_next(string=True)[2]
        album_url = html.find('span', string='Album').find_all_next(href=True)[0]['href']
    except AttributeError:
        err_timestamp = dt.datetime.now()
        u.log_this(f'{err_timestamp:%Y-%m-%d %H:%M} - scrape_song_url error: {url}')
        # print(f"Error finding album on {url}")
        album, album_url = "error", "error"

    return lyrics, album, album_url


def do_all_the_things(song_title, artist_name):
    response = search_song_artist(song_title, artist_name)
    if response.status_code != 200:
        return "error", "error", "error"

    url = get_song_url(response, artist_name)
    if url is None:
        return "error", "error", "error"

    lyrics, album, album_url = scrape_song_url(url)
    return lyrics, album, album_url


def scrape_album_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    rd_string1 = html.find('div', class_='metadata_unit').string
    rd_string2 = rd_string1.strip('Released ')
    release_date = dt.datetime.strptime(rd_string2, "%B %d, %Y")

    return release_date


def get_song_entry(entry, genre):
    raw_song, raw_artist = entry.split(' - ')
    song = re.split(song_splitter, raw_song)[0]
    artist = re.split(artist_splitter, raw_artist)[0]
    lyrics, alb, alb_url = do_all_the_things(song, artist)
    key = f'{song} - {artist}'
    return [key, {'song': song, 'artist': artist, 'album': alb, 'genre': genre, 'lyrics':lyrics}, alb_url]


def scrape_top_20(url):
    '''URL is of Billboard.com's top ~20 list.
    Returns a list that is comprised of song-artist entries.
        Example: ['Pyscho - Post Malone']
    '''
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')

    top_list = []
    for entry in html.findAll('div', class_='chart-list-item'):

        # artist
        test = entry.findAll('div', class_='chart-list-item__artist')
        for t in test:
            x = t.findAll('a')
            if x:
                artist = x[0].string.strip()
            else:
                x = t.string
                if x:
                    artist = x.strip()

        # song
        song = entry(class_='chart-list-item__title-text')[0].string.strip()

        top_list.append(f'{song} - {artist}')

    return top_list
