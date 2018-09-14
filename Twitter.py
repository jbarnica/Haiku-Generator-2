import configparser
import Haiku
import twitter

config = configparser.ConfigParser()
config.read('setup.ini')


def PostHaiku():
    api.PostUdpate(Haiku.get_haiku())

api = twitter.Api(
    consumer_key=config.get('Information', 'consumer_key', raw=False),
    consumer_secret=config.get('Information', 'consumer_secret', raw=False),
    access_token_key=config.get('Information', 'access_token_key', raw=False),
    access_token_secret=config.get('Information', 'access_token_secret', raw=False))




