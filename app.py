import praw
import subprocess
import scrapy
import nltk
import sqlite3, MySQLdb

from bot import comment
from getLinks import startScraping

def main():

    db_init()
    reddit_init()
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
                     passwd="Jame$9001",
                     db="posts")
    cursor = conn.cursor()

    #Creates table for already serviced posts
    query = 'CREATE TABLE IF NOT EXISTS posts_replied_to (post_id TEXT NOT NULL, artist TEXT NOT NULL, song TEXT NOT NULL)'
    cursor.execute(query)
    conn.commit()


'''
Initialize Reddit API wrapper
'''
def reddit_init():

    #Initialize bot1
    global reddit, subreddit
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit("hiphopheads")


'''
This bot gets and comments alternate streaming services for new song submissions
'''
def bot1():

    for submission in subreddit.new(limit=50):

        #Filter new posts for song submissions only
        newTitle = submission.title.lower()


        #Filter out soundcloud exclusive songs
        if "[fresh]" in newTitle and 'soundcloud' not in submission.url and len(newTitle.replace('[fresh]','').split('-')) == 2:

            print("Title: " + newTitle)
            print("Url: " + submission.url)
            query = 'SELECT post_id FROM posts_replied_to WHERE post_id="{}"'.format(submission.id)
            cursor.execute(query)
            servicedId = cursor.fetchone()

            # Only execute if post hasn't been replied to yet
            if not servicedId:

                #Parse the artist and song from the submission title
                artist = newTitle.replace('[fresh]','').split('-')[0].strip()
                song = newTitle.replace('[fresh]','').split('-')[1].strip()

                '''
                Initialize web scraper, get links
                '''
                startScraping()

                # Add submission to table of posts that have been replied to
                query = 'INSERT INTO posts_replied_to (post_id, artist, song) VALUES("{}","{}","{}")'.format(submission.id, artist, song)
                cursor.execute(query)
                conn.commit()



def bot2():
    return 0

if __name__=="__main__":
    main()
