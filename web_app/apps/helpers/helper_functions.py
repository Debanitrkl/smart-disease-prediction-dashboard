import numpy as np
import pandas as pd
import dash_html_components as html
import random
from textblob import TextBlob
import regex as re

df = pd.read_csv(r"E:\VIL Codefest\secret\frontend.csv")
tweets_df = pd.read_csv(r"E:\VIL Codefest\CustomDash\web_app\appdata\vodafoneidea_tweets.csv")
tweets = list(tweets_df['tweet'])


def get_location(customer):
    return df.iloc[customer]['Location']


def get_gender(customer):
    return df.iloc[customer]['Gender']


def get_age(customer):
    return df.iloc[customer]['Age']


def get_extended_values(value):
    operation = np.random.randint(0, 2)
    extended_values = []
    if operation:
        for i in range(6):
            i = np.random.randint(0, 100)
            extended_values.append(i + value)
    else:
        for i in range(6):
            i = np.random.randint(0, 100)
            extended_values.append(value - i)
    return extended_values


def get_segment(customer):
    return df.iloc[customer]['Customer Segment']


def get_churn(customer):
    return str(df.iloc[customer]['Churn']) + "%"


def get_tweets():
    a = re.sub(r"http\S+", "", random.choice(tweets))
    b = re.sub(r"http\S+", "", random.choice(tweets))
    c = re.sub(r"http\S+", "", random.choice(tweets))
    d = re.sub(r"http\S+", "", random.choice(tweets))
    e = re.sub(r"http\S+", "", random.choice(tweets))
    return html.Div([
        html.P(a, className='tweet'),
        html.P(b, className='tweet'),
        html.P(c, className='tweet'),
        html.P(d, className='tweet'),
        html.P(e, className='tweet'),
    ])


def get_polarity():
    n, p, neu = 0, 0, 0
    for tweet in tweets:
        blob = TextBlob(tweet)
        polarity = blob.sentiment[0]
        if polarity < 0:
            n += 1
        elif polarity > 0:
            p += 1
        else:
            neu += 1
    return [n, p, neu]
