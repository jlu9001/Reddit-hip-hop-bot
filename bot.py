'''
Bot functions
'''

import praw

#Initialize bot
def redditInit(bot):

    global reddit, subreddit
    reddit = praw.Reddit(bot)
    subreddit = reddit.subreddit("hiphopheads")


def comment(id, content):
    return 0

def post(id, content):
    return 0
