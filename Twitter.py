import configparser
import Haiku
import tweepy
import twitter
import Markov

import os

TWITTER_HANDLE = ''

FILE_NAME='twitter_list.txt'

def setup():
    global TWITTER_HANDLE
    config = configparser.ConfigParser()
    config.read('setup.ini')

    # Consumer keys and access tokens, used for OAuth
    consumer_key = config.get('Information', 'consumer_key', raw=False)              
    consumer_secret = config.get('Information', 'consumer_secret', raw=False)
    access_token = config.get('Information', 'access_token_key', raw=False)
    access_token_secret = config.get('Information', 'access_token_secret', raw=False)
    TWITTER_HANDLE = config.get('Information', 'handle', raw=False) 

    # OAuth process, using the keys and tokens       
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    return tweepy.API(auth)


def create_word_file(api):
    tweets = [status for status in tweepy.Cursor(api.user_timeline, screen_name=TWITTER_HANDLE).items()]        
    tweetText = [x.text for x in tweets]
    with open(FILE_NAME, 'w+') as f:        
        for i in tweetText:
            f.write('{}\n'.format(i.encode('utf8')))

def create_twitter_markov(api):
    try:
        with open(FILE_NAME, 'r') as f:
            file = f.read().replace('\n', '') 
    except IOError:
        create_word_file(api)
        with open(FILE_NAME, 'r') as f:
            file = f.read().replace('\n', '')   

    return Markov.get_model_from_block(file)

def CreateTwitHu():
    api = setup()    
    model = create_twitter_markov(api)
    for _ in range(1, 100):
        print('{}\n'.format(Haiku.find_poem(model,(5,7,5))))

if __name__ == "__main__":
    CreateTwitHu()
