"""
Name: sentiment.py
Purpose: Receives a list of tweets and pipelines the tweets through an open-source sentiment analysis model specificly tuned for twitter posts. The model will output 3 sentiment scores: negative, neutral, and positive. A simple match case will be used to translate the sentiment of the tweets into a short readable sentance, and returned for output.
Author: Kyle Bunn
"""

#import libraries
import pandas as pd
import torch
import tweepy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

#Function: sentiment_analysis(raw_tweets)
#Purpose: Receive list of tweets, and return a sentiment analysis of the tweets.
def sentiment_analysis(raw_tweets):
    
    #preprocess tweets to remove usernames and links
    tweet = []

    for index, row in raw_tweets.iterrows():
        line = row['text']
        new_line = [] # Create a new list to store the modified words
        for word in line.split():
            if word.startswith('@') and len(word) > 1:
                word = '@user'
            elif word.startswith('http'):
                word = "http"
                new_line.append(word) # Append modified words to the new list
                tweet.append(' '.join(new_line))

    #striped down tweets to only contain text. Useful to print() to see contents of messages
    tweet_proc = " ".join(tweet)


    # load open roBERTa model tuned for twitter posts
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    
    #load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(roberta)
    labels = ['Negative', 'Neutral', 'Positive']
    

    # sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    summary = []
    for i in range(len(scores)):
      s = scores[i]
      summary.append(s)
    
    final_summary = []
    match summary.index(max(scores)):
      case 0:
          final_summary.append(str("{:.0%}".format(summary[0])))
          final_summary.append("Negative")
      case 1:
          final_summary.append(str("{:.0%}".format(summary[1])))
          final_summary.append("Neutral")
      case 2:
          final_summary.append(str("{:.0%}".format(summary[2])))
          final_summary.append("Positive")
          
    output = " ".join(final_summary)
    #print(output)
    return output
    