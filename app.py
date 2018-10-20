import praw
import scrapy
import nltk

def main():
    bot1_init()

'''
This bot gets and comments alternate streaming services for new song submissions
'''
def bot1_init():

    #Initialize bot1
    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit("hiphopheads")
    for submission in subreddit.hot(limit=50):
        if "[fresh]" in submission.title.lower():
            print("Title: ", submission.title)
            print("Text: ", submission.selftext)



if __name__=="__main__":
    main()
