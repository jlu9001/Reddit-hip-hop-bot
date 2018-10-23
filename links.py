'''
Use beautifulSoup to scrape streaming services for song links
'''

import requests
from bs4 import BeautifulSoup

def getLinks(song, artist):

    services = ['Spotify', 'Apple+Music', 'Amazon+Music', 'Google+Play', 'Tidal']
    url = "https://www.google.com/search?q="

    '''
    Scrape links
    '''


    links = {"Spotify":"", "Apple Music":"", "Amazon Music":"", "Google Play":"", "Tidal":""}
    return links
