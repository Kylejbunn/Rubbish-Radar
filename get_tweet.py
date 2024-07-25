"""
Name: get_tweet.py
Purpose: Connect to twitter api and retrieve a sample of 10 tweets from a given search term. Strip unnecessary data from tweets and pass a list of tweets to sentiment.py for sentiment analysis. Returns a string consisting of the sentiment analysis of the tweets and the highest sentiment score out of 100%.
Author: Kyle Bunn
"""

#import libraries 
import pandas as pd
import tweepy
import os
import html
import sentiment

# enviorment security varibles
bearer_token = os.environ['bearer_token']
api_key = os.environ['api_key']
api_key_secret = os.environ['api_key_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']

#Function: get_Tweets(search_term))
#Purpose: Connect to twitter api and retrieve a sample of 10 tweets from a given search term. Includes a simple text sanitization function strip unnecessary data from user input.

def get_tweet(tweet_search):
  sanitized_message = html.escape(tweet_search)
  
  
  # Twitter API authentication
  client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
  auth = tweepy.OAuthHandler(api_key, api_key_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

#This is the primary search function of the program. It takes a search term and returns a list of tweets. Current x.com api restricts the number of tweets returned per 15min period to 15 tweets but no less then 10 per single request. 
  try:  
    sample = client.search_recent_tweets(query=sanitized_message, max_results=10)
  except:
    return (f"Error: Too many requests. Please try again in 15 minutes.")
  
  raw_tweets = pd.DataFrame(sample.data)
  raw_tweets = raw_tweets[['text']]

#This function takes a list of tweets and returns a sentiment analysis of the tweets.
  sentiment_score = sentiment.sentiment_analysis(raw_tweets)

#This function constructs a simple output sentance from the sentiment analysis of the tweets.
  summary = "Recent tweets about" + " " + tweet_search + " " + "are" + " " + sentiment_score
  
  return summary



def debug():
  sanitized_message = "Elon Musk"
  # Twitter API authentication
  client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
  auth = tweepy.OAuthHandler(api_key, api_key_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)
  print("Twitter: Connection Successful")

#This is the primary search function of the program. It takes a search term and returns a list of tweets. Current x.com api restricts the number of tweets returned per 15min period to 15 tweets but no less then 10 per single request. 
  try:  
    sample = client.search_recent_tweets(query=sanitized_message, max_results=10)
    print("Twitter: Search Successful")
  except:
    return (f"Error: Too many requests. Please try again in 15 minutes.")

  raw_tweets = pd.DataFrame(sample.data)
  raw_tweets = raw_tweets[['text']]
  print(raw_tweets)

#This function takes a list of tweets and returns a sentiment analysis of the tweets.
  sentiment_score = sentiment.sentiment_analysis(raw_tweets)
  print("Machine Learning: Tokenization Successful")
  print("Machine Learning: Sentiment Analysis Successful")
#This function constructs a simple output sentance from the sentiment analysis of the tweets.
  summary = "Recent tweets about" + " " + sanitized_message + " " + "are" + " " + sentiment_score

  return summary