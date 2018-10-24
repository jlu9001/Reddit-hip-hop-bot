'''
Use beautifulSoup to scrape streaming services for song links
'''

import requests
from bs4 import BeautifulSoup

def getLinks(song, artist):

    # Replace spaces with addition symbols for google search query
    query = song.replace(' ', '+') + '+by+' + artist.replace(' ', '+')

    services = ['Spotify', 'Apple+Music', 'Amazon+Music', 'Google+Play', 'Tidal']

    for service in services:

        # Create google search query
        url = "https://www.google.com/search?q="
        url += query + '+' + service
        print(url)

        '''
        Scrape links
        '''


    links = {"Spotify":"", "Apple Music":"", "Amazon Music":"", "Google Play":"", "Tidal":""}
    return links
