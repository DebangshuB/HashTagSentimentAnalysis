# HashTag Sentiment Analysis
## Introduction
The model takes in a keyword or hashtag and returns the average sentiment around the given keyword / hashtag.

Dataset used was the [Kaggle Sentiment140 Dataset ](https://www.kaggle.com/kazanova/sentiment140) consisting of 1.6 million tweets. The model was developed and trained on Google Colab using thier GPUs. The Frontend and Backend of the web app were added subsequently.

![](https://img.shields.io/badge/python-3.8.11-brightgreen)
![](https://img.shields.io/badge/tensorflow-2.3.0-yellowgreen)
![](https://img.shields.io/badge/numpy-1.19.5-orange)
![](https://img.shields.io/badge/tweepy-3.10.0-lightgrey)
![](https://img.shields.io/badge/nltk-3.6.2-blue)
![](https://img.shields.io/badge/node-14.16.0-brightgreen)
![](https://img.shields.io/badge/npm-6.14.11-yellow)
![](https://img.shields.io/badge/express-4.17.1-red)
![](https://img.shields.io/badge/python--shell-3.0.0-orange)


![](images/2.png)
---

## The Dataset and Preprocessing
The dataset used was [Kaggle Sentiment140 Dataset ](https://www.kaggle.com/kazanova/sentiment140) as stated above. The dataset consists of 1.6 millions tweets containing 6 columns out of which I only used 2 :-
* The Body of the tweet 
* The target labels 
    * 4 : Positive 
    * 0 : Negative

Changed the labels to be 1 for Positive and kept Negatives the same.

### Preprocessing
Removed all urls, tags, hashtags and stemming. Words with very low occurences were deleted to avoid crazy memory requirements. After applying the required transformations on the Train, Test and Validation split they were padded for the LSTM cells.


## The Deep Learning Model
The Embedding layer size was fixed on 5 with a single LSTM cell following. Dropout Regularization with 40% dropout inbetween 2 Dense layers. 
Trained for 200 epochs. Test score was just as good as validation score.


## Predictions
Live predictions used tweepy to get tweets.

**Note : To run the project you will have to replace the dummy access tokens with your own.**


## Backend and Frontend
Backend using Nodejs and Express. [Python-shell](https://www.npmjs.com/package/python-shell) to run the python script for predictions.

Frontend made of basic of HTML, CSS and JS with Chart.js.
