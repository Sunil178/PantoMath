import numpy as np
import pandas as pd
import tweepy
import json
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
API_KEY="BB8uhuyrMzHesokpE7RqcYemc"
API_SECRET="7YhL2UOSVoUyquuImiT1uOag0gS5HR3mrt7mmXrNZbwNHOVklF"
ACCESS_TOKEN="2330384770-kx4jr7mfUsCJod2MNuff3VzCh6tbGCvdymwp3ND"
ACCESS_TOKEN_SECRET="IMEYoDK2gZITSztqKQvHohTMOPkmEjsA0w6AOoECIdCqu"
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
obj = tweepy.API(auth)
no = 0
tweets = []
entitylist = lst
i = 0
listindex = 0
class MyStreamListener(tweepy.StreamListener):
   def on_data(self, data):
       global no
       global listindex
       no += 1
       data = json.loads(data)
       print(no, end = " ")
       tweets.append(data['text'])
       if no == 1000:
           no = 0
           return False
   def on_status(self, status):
       global entitylist, i
       myStreamListener = MyStreamListener()
       myStream = tweepy.Stream(auth = obj.auth, listener = myStreamListener)
       myStream.filter(track = [entitylist[i]])
   def on_error(self, status_code):
       if status_code == 420:
           return False
streamListener = MyStreamListener()
for entity in entitylist:
    streamListener.on_status("success")
    i += 1


stopwords = stopwords.words("english")
punctuation = string.punctuation
sent_tokenized_list = []
tweet_list_new = []
words = []

for tweet in tweets:
    sent_tokenized_list.append(sent_tokenize(tweet))
    for sent in sent_tokenized_list:
        sent = "".join(sent)
        for char in punctuation:
            if char in sent:
                sent = sent.replace(char, '')
        words.append(word_tokenize(sent))
        for word in stopwords:
            if word in words[0]:
                words[0].remove(word)
        sent = " ".join(words[0])
        tweet_list_new.append(sent)
        words = []
    sent_tokenized_list = []

dic = {'Tweets': tweet_list_new}
df = pd.DataFrame(dic)
df.to_csv('tweets.csv')
print(tweet_list_new)