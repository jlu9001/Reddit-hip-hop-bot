'''
Created by James Lu.
Last Modified: 10/22/2018
Usage: $ python3 app.py <MySQL Password>
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

    db_init()
    bot1 = Bot1()

    links = getLinks("I Love It","Kanye West")
    print(links)
    #comment("9bl2uu","Yeezy yeezy what's good")

    '''
    while(1):
        bot1.run()
    '''

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

                        print("Title: " + newTitle)
                        print("Url: " + child["data"]["url"])
                        artist = newTitle.replace('[fresh]','').split('-')[0].strip()
                        song = newTitle.replace('[fresh]','').split('-')[1].strip()
                        links = getLinks(song, artist)


                        query = 'SELECT post_id FROM posts_replied_to WHERE post_id="{}"'.format(child["data"]["id"])
                        cursor.execute(query)
                        servicedId = cursor.fetchone()

                        # Only execute if post hasn't been replied to yet
                        if not servicedId:

                            artist = newTitle.replace('[fresh]','').split('-')[0].strip()
                            song = newTitle.replace('[fresh]','').split('-')[1].strip()
                            id = child["data"]["id"]

                            #Get links from streaming services
                            links = getLinks(song, artist)

                            #Comment to post
                            comment=""
                            #comment(id, comment)


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
