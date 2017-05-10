import tweepy
import re
import redditbot
from time import sleep
from credentials import *
from textblob import TextBlob

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

response = "Hello! @"
post = " here is a top post this week from /r/"
default_subreddit = 'memeeconomy'
#url = redditbot.get_top_posts(default_subreddit) #default subreddit

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t:_])|(\w+:\/\/\S+)", " ", tweet).split())
def reply(subreddit):
    url = redditbot.get_top_posts(subreddit)
    return url

def default_response():
    print('I do not understand that. Common commands are ')
    help()
    return """I do not understand that. Common commands are:
        random, top_post:(subreddit name), sentiment_analysis:(argument)"""

def help():
    print ('command words: random, top_post:(subreddit name), sentiment_analysis:(argument)')

def get_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'This topic was dank'
    elif analysis.sentiment.polarity == 0:
        return 'This topic is neutral'
    elif analysis.sentiment.polarity < 0:
        return 'This topic was not dank'

def get_tweets(query,count = 10):
    tweets = [ ]
    positive_tweets = [ ]
    try:
        fetched = api.search(q = query,count = count)
        for tweet in fetched:
            tweets.append(tweet)
            if get_sentiment(tweet.text) == 'This topic was dank':
                positive_tweets.append(tweet)
        if len(positive_tweets)/len(tweets) > .5:
            return 'This topic was dank'
        elif len(positive_tweets)/len(tweets) == .5:
            return 'This topic is neutral'
        else:
            return 'This topic was not dank'

    except tweepy.TweepError as e:
        print(e.reason)


def read_tweet(tweet,screen_name,idnum):
    command = clean_tweet(tweet) #TODO current cleaning gets rid of underscores and colons
    #command = tweet
    print (command)
    if command == 'random':
        #post random top post
        print (reply(default_subreddit))
        url = reply(default_subreddit)
        api.update_status(response+screen_name+post+
            default_subreddit+" "+url,in_reply_to_status_id = idnum)
        #return reply(default_subreddit)
    elif command.startswith('top_post:'):
        #post top post from specified subreddit
        keyword = ':'
        before_keyword, keyword, after_keyword = command.partition(keyword)
        print (reply(after_keyword))
        url = reply(after_keyword)
        api.update_status(response+screen_name+post+
            after_keyword+" "+url,in_reply_to_status_id = idnum)
        #return reply(after_keyword)
    elif command.startswith('sentiment_analysis:'):
        #analysis on that word
        keyword = ':'
        before_keyword, keyword, after_keyword = command.partition(keyword)
        #print (get_sentiment(after_keyword))
        answer = get_tweets(after_keyword)
        api.update_status(response+screen_name+" "+answer,in_reply_to_status_id = idnum)
        #return get_sentiment(after_keyword)
    else:
        answer = default_response()
        api.update_status(answer, in_reply_to_status_id = idnum)




while True:
    tweets = tweepy.Cursor(api.search,q="@deidaraxc4bot").items(5)
    try:
        for tweet in tweets:
            tweetid = tweet.id
            name = tweet.user.screen_name
            #test
            #print(clean_tweet(tweet.text))
            #print (tweet.text)
            #print ('************posting dank meme*************')
            if tweet.text.startswith('@deidaraxc4bot'):
                read_tweet(tweet.text,name,tweetid)
            #print (response+tweet.user.screen_name+post+default_subreddit+
            #    " "+url)
            #api.update_status(response+tweet.user.screen_name+post+
                #subreddit+" "+url,in_reply_to_status_id = tweetid)
            sleep(10)

    except tweepy.TweepError as e:
        print(e.reason)

    except StopIteration:
        break
    print ('going to sleep for 60seconds')
    sleep(60)
