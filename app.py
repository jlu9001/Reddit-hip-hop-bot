'''
Main application. Execute via
'''

import os, sys
import requests, json
import numpy, matplotlib, nltk
import sqlite3, MySQLdb

from bot import redditInit, comment, post
from links import getLinks

def main():

    db_init()

    #main program
    while(1):
        bot1()
        bot2()


'''
Initialize SQL database to store Reddit posts
'''
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


'''
This bot gets and comments alternate streaming services for new song submissions
'''
def bot1():

    redditInit('bot1')

    response = json.loads(requests.get("https://www.reddit.com/r/hiphopheads/new.json?sort=new").text)

    #Check for valid response from Reddit API
    try:
        if response["data"]:

            # Get array of new posts
            children = response["data"]["children"]
            for child in children:

                #Filter new posts for song submissions only
                newTitle = child["data"]["title"].lower()
                if "[fresh]" in newTitle and 'soundcloud' not in child["data"]["url"] and len(newTitle.replace('[fresh]','').split('-')) == 2:

                    print("Title: " + newTitle)
                    print("Url: " + child["data"]["url"])
                    query = 'SELECT post_id FROM posts_replied_to WHERE post_id="{}"'.format(child["data"]["id"])
                    cursor.execute(query)
                    servicedId = cursor.fetchone()

                    # Only execute if post hasn't been replied to yet
                    if not servicedId:
                        artist = newTitle.replace('[fresh]','').split('-')[0].strip()
                        song = newTitle.replace('[fresh]','').split('-')[1].strip()

                        #initialize web scraper, get links

                        # Add submission to table of posts that have been replied to
                        query = 'INSERT INTO posts_replied_to (post_id, artist, song) VALUES("{}","{}","{}")'.format(child["data"]["id"], artist, song)
                        cursor.execute(query)
                        conn.commit()

    except:
        print("No response")
        return 0


def bot2():
    return 0

if __name__=="__main__":
    main()
