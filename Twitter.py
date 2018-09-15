import configparser
import Haiku
import twitter

TWITTER_HANDLE = ''

def user_tweet(num, thandle):
    statuses = api.GetUserTimeline(screen_name=thandle)
    tweetList = [statuses[x].text for x in range(num)]
    return tweetList

def post_haiku():
    api.PostUpdate(Haiku.get_haiku())

def setup():
    global TWITTER_HANDLE
    config = configparser.ConfigParser()
    config.read('setup.ini')

    TWITTER_HANDLE = config.get('Information', 'handle', raw=False)

    api = twitter.Api(
        consumer_key=config.get('Information', 'consumer_key', raw=False),
        consumer_secret=config.get('Information', 'consumer_secret', raw=False),
        access_token_key=config.get('Information', 'access_token_key', raw=False),
        access_token_secret=config.get('Information', 'access_token_secret', raw=False))        
    return api

def get_latest_tweet():
    return user_tweet(1, TWITTER_HANDLE)

def get_tweets(num):
    return user_tweet(num, TWITTER_HANDLE)

if __name__ == "__main__":    
    api = setup()
    if api.VerifyCredentials():
        for i in get_tweets(10):
            print(Haiku.haiku_from_tweet(i))


