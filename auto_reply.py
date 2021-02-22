import ConfigParser
import json
import tweepy
 
from nltk.chat import eliza
from random import randint
 
 
config = ConfigParser.ConfigParser()
config.read('.twitter')
 
consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
account_screen_name = config.get('rule', 'name')
account_user_id = config.get('rule', 'uid')
 


 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
twitterApi = tweepy.API(auth)
 
chatbot = eliza.Chat(eliza.pairs)
 
class ReplyToTweet(tweepy.StreamListener):
 
    def on_data(self, data):
        #print data
        tweet = json.loads(data.strip())
       
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id
        rand=randint(1,7)
        #print "re" + retweeted
        #print "from" + from_self
 
        if retweeted is not None and not retweeted and not from_self:
 
            
 
            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')
            respondText='this is auto message'.decode('utf-8')
 
            replyText = '@' + screenName + ' ' + respondText
 
            #check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:137] + '...'
 
            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)
            
 
            # If rate limited, the status posts should be queued up and sent on an interval
            twitterApi.update_status(status=replyText, in_reply_to_status_id=tweetId)
 
    def on_error(self, status):
        print status
 
if __name__ == '__main__':
    trackName = '@user'
    streamListener = ReplyToTweet()
    twitterStream = tweepy.Stream(auth, streamListener)
    twitterStream.filter(track=([trackName]))