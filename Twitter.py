import configparser
import Haiku
import twitter
import Markov
import re
import os

TWITTER_HANDLE = ''

def user_tweet(num, thandle):
    statuses = api.GetUserTimeline(screen_name=thandle)
    tweetList = [statuses[x].text for x in range(num)]
    return tweetList

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

def get_tweets(num):
    return user_tweet(num, TWITTER_HANDLE)

def get_latest_tweet():
    return get_tweets(1)

def create_twitter_markov(api, thandle):
    tweets = api.GetUserTimeline(screen_name=thandle, count=200, include_rts=False, exclude_replies=True)
    tweetText = [x.text for x in tweets]
    return Markov.get_Model(tweetText)

def strip_text(text):
    return re.sub("^\s+|\s+$", "", text, flags=re.UNICODE)

def copy_text(text):
    """Python string copying sucks"""
    return ' '.join(text.split(" "))

def create_Twitter_Line(model, num):
    corpus = Haiku.get_dict()

    #gotta clean this all up....
    while True:
        originalText = model.make_sentence()
        if originalText:
            text = copy_text(originalText)
            while text and ' ' in text and text !=  ' ':
                if all([corpus.get(x.lower()) for x in text.split(' ')]):
                    if Haiku.check_syllables(text, corpus) == num:
                        return text
                text = text[:text.rindex(' ')]
                text = strip_text(text)
            text = copy_text(originalText)
            while text and ' ' in text and text !=  ' ':
                if all([corpus.get(x.lower()) for x in text.split(' ')]):
                    if Haiku.check_syllables(text, corpus) == num:
                        return text
                text = text[:text.rindex(' ')]
                text = strip_text(text)
            text = copy_text(originalText)
            while text and ' ' in text and text !=  ' ':
                if all([corpus.get(x.lower()) for x in text.split(' ')]):
                    if Haiku.check_syllables(text, corpus) == num:
                        return text
                text = text[text.index(' '):]
                text = strip_text(text)
            text = copy_text(originalText)
            while text and ' ' in text and text !=  ' ':
                if all([corpus.get(x.lower()) for x in text.split(' ')]):
                    if Haiku.check_syllables(text, corpus) == num:
                        return text
                text = text[text.index(' '):text.rindex(' ')]
                text = strip_text(text)             

def CreateTwitHu():
    api = setup()
    if api.VerifyCredentials():
        model = create_twitter_markov(api, TWITTER_HANDLE)
        for i in range(1, 100):
            print("{}\n{}\n{}\n\n".format(
                create_Twitter_Line(model, 5),
                create_Twitter_Line(model, 7),
                create_Twitter_Line(model, 5)
                )
            )
def CreateChains():
    with open("output.txt", 'a') as f:
        api = setup()
        if api.VerifyCredentials():
            model = create_twitter_markov(api, TWITTER_HANDLE)
            for i in range(100):
                output = model.make_sentence()
                if output is not None:
                    f.write("{}\n".format(output))

if __name__ == "__main__":
    CreateTwitHu()