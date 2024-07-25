"""
Name: Rubbush Radar
Purpose: Allows a discord user to sample social media posts, and receive a summary of the sentiments expressed in the posts.
Author: Kyle Bunn
"""

#import libraries 
import pandas
import os
import discord
from discord import Client, Intents, Message
import get_tweet


#Enviroment security variables
disc_token = os.environ['discord_token']

#Discord Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#Bot Commands:
#confirm successful connection to discord
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#respond to user message
@client.event
#unless the last user message was from yourself, dont make endless loops.
async def on_message(message):
  if message.author == client.user:
    return
  #Simple hello message for testing
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  #Simple hello message for testing
  if message.content.startswith('$debug'):
    debug_test = get_tweet.debug()
    await message.channel.send(debug_test)

  #Seach recent tweets for a given search term
  #Example '$tweet John Lennon'
  if message.content.startswith('$tweet'):
    tweet_search = message.content.split('$tweet ', 1)[1]
    tweet_text = get_tweet.get_tweet(tweet_search)
    await message.channel.send(tweet_text)

client.run(disc_token)