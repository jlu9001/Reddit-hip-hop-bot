'''
Bot functionality
'''

import praw

#Initialize bot
def redditInit(bot):

    global reddit, subreddit
    reddit = praw.Reddit(bot)
    subreddit = reddit.subreddit("jlu9001")


#Posts comment to a submission
def comment(postId, content):

    submission = reddit.submission(id=postId)
    submission.reply(content)


#Posts submission to subreddit
def post(id, content):
    return 0
