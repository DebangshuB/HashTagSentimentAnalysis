#!/usr/bin/env python
# coding: utf-8


# Imported for DL
import tensorflow as tf
import numpy as np

# Imported for Preprocessing
from nltk.stem import PorterStemmer
import re
import json

# Scripting
import sys
import os

# Impoorted For Scraping Tweets
import tweepy

# Set-up for Tweepy
consumer_key = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

path = os.path.dirname(os.path.abspath(__file__))

# Setting up parameters for preprocessing
f = open(os.path.join(path, './static/parameters.json'))
parameters = json.load(f)

max_padding_length = parameters['max_len']
word2idx = parameters['word2idx']
INPUT_DIM = parameters['input_dim']
OUTPUT_DIM = parameters['output_dim']
INPUT_LEN = parameters['input_len']
BATCH_SIZE = parameters['batch_size']


# Setting up the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(input_dim=INPUT_DIM +
          1, output_dim=OUTPUT_DIM, input_length=INPUT_LEN))
model.add(tf.keras.layers.LSTM(64))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.4))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# Loading Weights
model.load_weights(os.path.join(path, './static/weights/'))

# Function for Preprocessing


def process_text(text):
    # Lowercasing
    text = text.lower()

    # Replacing all the urls
    text = re.sub('(?i)\\b((?:https?://|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)(?:[^\\s()<>]+|\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\))+(?:\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\)|[^\\s`!()\\[\\]{};:\'\\".,<>?\xc2\xab\xc2\xbb\xe2\x80\x9c\xe2\x80\x9d\xe2\x80\x98\xe2\x80\x99]))', '', text)

    # Replacing all user tags
    text = re.sub(r"@[^\s]+", '', text)

    # Replacing all hashtags
    text = re.sub(r"#[^\s]+", '', text)

    # Remove some punctuations
    text = re.sub(r"[!?,'\"*)@#%(&$_.^-]", '', text)

    # Splitting on spaces
    text = text.split(' ')

    # Stemming and removing spaces
    stemmer_ps = PorterStemmer()
    text = [stemmer_ps.stem(word) for word in text if len(word)]

    # Mapping the words to numbers for the embedding layer
    text = [word2idx[word] for word in text if word in word2idx]

    # Making Numpy
    text = np.array(text)
    text = np.reshape(text, (1, -1))

    # Padding for LSTM layers
    text = tf.keras.preprocessing.sequence.pad_sequences(
        text, padding='post', maxlen=max_padding_length)

    return text


def work(number_of_tweets, topic):
    # Actual Code
    tweets_ = []
    tweets = []
    y_pred = []

    for tweet in tweepy.Cursor(api.search, q=topic + ' -filter:retweets', lang="en", tweet_mode='extended').items(number_of_tweets):
        tweets_.append(tweet.full_text)

    for i in range(len(tweets_)):
        tweets_[i] = process_text(tweets_[i])

    for i in range(len(tweets_)):
        if sum(tweets_[i][0]) == 0:
            continue
        tweets.append(tweets_[i])

    y_pred = []

    for tweet in tweets:
        y_pred.append(model.predict(tweet)[0][0])

    result = ""
    for i in y_pred:
        result += "{:.2f},".format(i)

    return result
