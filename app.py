'''
Created by James Lu.
Last Modified: 10/22/2018
Usage: $ python app.py <MySQL Password>
'''

import os, sys
import requests, json
import numpy as np
import matplotlib, nltk
import MySQLdb

from bot import redditInit, comment, post
from links import getLinks


#Main program
def main():

    # Initialize database and bots
    db_init()
    bot1 = Bot1()

    while(1):
        bot1.run()

#Initialize SQL database to store Reddit posts
def db_init():

    #Initialze database
    global conn, cursor
    conn = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd=os.environ['SQLPASS'],
                     db="posts")
    cursor = conn.cursor()

    #Creates table for already serviced posts
    query = 'CREATE TABLE IF NOT EXISTS posts_replied_to (post_id TEXT NOT NULL, artist TEXT NOT NULL, song TEXT NOT NULL)'
    cursor.execute(query)
    conn.commit()


#This bot gets and comments alternate streaming services for new song submissions
class Bot1():

    def __init__(self):
        redditInit('bot1')

    def run(self):

        #Check for valid response from Reddit API
        response = json.loads(requests.get("https://www.reddit.com/r/hiphopheads/new.json?sort=new", timeout=5).text)
        try:
            if response["data"]:

                # Get array of new posts
                children = response["data"]["children"]
                for child in children:

                    #Filter new posts for song submissions only and filter out songs exclusive to soundcloud
                    newTitle = child["data"]["title"].lower()
                    if "[fresh]" in newTitle and 'soundcloud' not in child["data"]["url"] and len(newTitle.replace('[fresh]','').split('-')) == 2:

                        query = 'SELECT post_id FROM posts_replied_to WHERE post_id="{}"'.format(child["data"]["id"])
                        cursor.execute(query)
                        servicedId = cursor.fetchone()

                        # Only execute if post hasn't been replied to yet
                        if not servicedId:

                            artist = newTitle.replace('[fresh]','').split('-')[0].strip()
                            song = newTitle.replace('[fresh]','').split('-')[1].strip()
                            id = child["data"]["id"]

                            print("Song: " + song)
                            print("Artist: " + artist)
                            print("Getting links")


                            #Get links from streaming services
                            links = getLinks(song, artist)

                            #Comment to post
                            content="Here are other streaming services that have " + song.upper() + " by " + artist.upper()+ ":\n***\n" \
                                    + (("[Spotify](" + links["Spotify"] + ")\n\n") if 'open.spotify' in links["Spotify"] and 'user' not in links["Spotify"] else "Spotify Link Unavailable\n\n") \
                                    + (("[Apple Music](" + links["Apple Music"] + ")\n\n") if 'itunes.apple' in links["Apple Music"] else "Apple Music Link Unavailable\n\n") \
                                    + (("[Amazon Music](" + links["Amazon Music"] + ")\n\n") if 'amazon' in links["Amazon Music"] else "Amazon Music Link Unavailable\n\n") \
                                    + (("[Google Play](" + links["Google Play"] + ")\n\n") if 'play.google' in links["Google Play"] else "Google Play Link Unavailable\n\n") \
                                    + (("[Tidal](" + links["Tidal"] + ")\n\n") if 'tidal.com' in links["Tidal"] else "Tidal Link Unavailable\n\n") \
                                    + "***\n^(I am a bot. You can view my source code) ^[here](https://github.com/jlu9001/Reddit-hip-hop-bot)"

                            comment(id, content)

                            print("Serviced id: " + id)

                            # Add submission to table of posts that have been replied to
                            query = 'INSERT INTO posts_replied_to (post_id, artist, song) VALUES("{}","{}","{}")'.format(id, artist, song)
                            cursor.execute(query)
                            conn.commit()

        except:
            return 0


#This bot analyzes user sentiments in new album threads
class Bot2():
    def __init__(self):
        return 0

if __name__=="__main__":
    main()
