import praw
import scrapy
import nltk
import sqlite3, MySQLdb

def main():

    db_init()
    bot1_init()


'''
Initialize SQL database to store Reddit posts
'''
def db_init():

    #Initialze database
    global conn, cursor
    conn = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="Jame$9001",  # your password
                     db="posts")        # name of the data base
    cursor = conn.cursor()

    #Creates table for already serviced posts
    query = 'CREATE TABLE IF NOT EXISTS posts_replied_to (post_id TEXT NOT NULL, artist TEXT NOT NULL, song TEXT NOT NULL)'
    cursor.execute(query)
    conn.commit()


'''
This bot gets and comments alternate streaming services for new song submissions
'''
def bot1_init():

    #Initialize bot1
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit("hiphopheads")
    for submission in subreddit.hot(limit=50):

        #Filter new posts for song submissions only
        newTitle = submission.title.lower()

        if "[fresh]" in newTitle:
            print("Title: ", newTitle)

        if "[fresh]" in newTitle and len(newTitle.replace('[fresh]','').split('-')) <= 2:

            query = 'SELECT post_id FROM posts_replied_to WHERE post_id="{}"'.format(submission.id)
            cursor.execute(query)
            servicedId = cursor.fetchone()

            # Only execute if post hasn't been replied to yet
            if not servicedId:

                #Parse the artist and song from the submission title
                artist = newTitle.replace('[fresh]','').split('-')[0].strip()
                song = newTitle.replace('[fresh]','').split('-')[1].strip()



                # Add submission to table of posts that have been replied to
                query = 'INSERT INTO posts_replied_to (post_id, artist, song) VALUES("{}","{}","{}")'.format(submission.id, artist, song)
                cursor.execute(query)
                conn.commit()


if __name__=="__main__":
    main()
