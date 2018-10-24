'''
Use beautifulSoup to scrape web for song links
'''

import requests
from bs4 import BeautifulSoup

def getLinks(song, artist):

    # Replace spaces with addition symbols for google search query
    query = song.replace(' ', '+') + '+by+' + artist.replace(' ', '+')

    links = {"Spotify":"", "Apple Music":"", "Amazon Music":"", "Google Play":"", "Tidal":""}
    services = ['Spotify', 'Apple Music', 'Amazon Music', 'Google Play', 'Tidal']

    for service in services:

        # Create google search query
        url = "https://www.google.com/search?q="
        url += query + '+' + service.replace(' ','+')

        # Fetch content from url
        response = requests.get(url, timeout=5)
        content = BeautifulSoup(response.content, "html.parser")
        link = content.find(attrs={"class": "r"}).a.get('href')     # Scrape top link from google

        # Clean the link
        link = link.replace('/url?q=', '')
        link = link[0:link.find("&sa=")].replace("%3F",'?').replace("%3D",'=').replace("%26", '&').replace(')','\)')

        links[service]=link


    return links
