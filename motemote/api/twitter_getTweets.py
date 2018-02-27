# encoding: utf-8
# author: Tomoya
# created_at: 2017/12/01

import tweepy

class TweetGetter(object):
    CK = "KINHRDJKDjXxjf0Y9WMPuE09q"
    CS = "UwVaMjr6bEOK1WquNDOMCsSmZc2phVangJkvy7TU3zYXjsrKVH"
    AT = "883630081473617921-5EHbdHAPn7MURLhFtD0uewHvMQPs3X2"
    AS = "0ObJeBCW2yszFr8elB8PDGxi24JEoVpxmTSAbELucy9oe"
    
    def __init__(self, CK=CK,CS=CS,AT=AT,AS=AS):
        auth = tweepy.OAuthHandler(CK, CS)
        auth.set_access_token(AT, AS)
        self.API = tweepy.API(auth, api_root='/1.1', wait_on_rate_limit=True)

    def getFollowerIds(self, screenName):
        followerIds = []
        try:
            followers = tweepy.Cursor(self.API.followers_ids, id = screenName, cursor = -1).items()
            for follower in followers:
                followerIds.append(follower)
        except tweepy.error.TweepError as et:
            print(et.reason)
        return followerIds
    
    def getTimelineTextsFavos(self, screenName, limit=200):
        tweetTexts = []
        tweetFavos = []
        try:
            tweets = tweepy.Cursor(self.API.user_timeline, screen_name=screenName, exclude_replies = True).items()
            for cnt, tweet in enumerate(tweets):
                if not cnt < limit:
                    break
                tweetTexts.append(tweet.text)
                tweetFavos.append(tweet.favorite_count)
        except tweepy.error.TweepError as et:
            print(et.reason)
        return tweetTexts, tweetFavos
