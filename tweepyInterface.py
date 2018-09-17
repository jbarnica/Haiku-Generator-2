import tweepy
import configparser

def get_Details():
    config = configparser.ConfigParser()
    config.read('setup.ini')

    # Consumer keys and access tokens, used for OAuth
    consumer_key=config.get('Information', 'consumer_key', raw=False)              
    consumer_secret=config.get('Information', 'consumer_secret', raw=False)
    access_token=config.get('Information', 'access_token_key', raw=False)
    access_token_secret=config.get('Information', 'access_token_secret', raw=False)

    # OAuth process, using the keys and tokens       
    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)

    for status in tweepy.Cursor(api.user_timeline, screen_name='@realDonaldTrump').items():
        print(status._json['text'])


if __name__ == "__main__":
    get_Details()